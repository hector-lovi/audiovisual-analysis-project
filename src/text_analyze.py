from googletrans import Translator
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk import sent_tokenize, word_tokenize
import nltk
from gensim import corpora, models
import gensim
import string
import pandas as pd
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Crear una clase que inicie keras y carge el modelo,
# seguido del resto de funciones para realizar el análisis visual y textual.


def detectLanguage(txt):
    '''
    Detecta el idioma del texto.
    '''
    translator = Translator()
    detect = translator.detect(txt)
    return detect.lang


def translateLanguage(txt, dest):
    '''
    Traduce el texto al destino que le indiques.
    '''
    translator = Translator()

    return translator.translate(txt, dest=str(dest)).text


def textSentiment(txt):
    '''
    Realiza un análisis de sentimiento sobre un texto en crudo (sin filtro).
    Funciona tanto en inglés como en español.
    '''
    if detectLanguage(txt) != 'es' or detectLanguage(txt) != 'en':
        txt = translateLanguage(txt, 'en')

    s = SentimentIntensityAnalyzer()
    result = s.polarity_scores(txt)
    return str(result)


def cleanText(txt):
    '''
    Dividir el texto en palabras y extraemos contenido que no aporta información
    como stop words y signos de puntuación.
    '''
    # Detectamos el idioma del texto.
    # Si es diferente al español, lo traducimos.
    detect = detectLanguage(txt)
    if detect != 'es':
        txt = translateLanguage(txt, 'es')

    # Dividir el texto en palabras.
    palabras = word_tokenize(txt.lower())

    # Palabras que no aportan valor en el análisis.
    stop_word = stopwords.words('spanish')

    # Limpieza de palabras.
    palabras = [p for p in palabras if p not in stop_word +
                list(string.punctuation)]
    return palabras


def freqWords(palabras):
    '''
    Reducir las palabras a su raiz.
    Top 5 de las palabras más repetidas del texto.
    '''
    stemmer = SnowballStemmer('spanish')

    raices = []
    for palabra in palabras:
        raices.append(stemmer.stem(palabra))

    freq = FreqDist(raices).most_common(5)
    return str(freq)


def preprocessing(txt):
    '''
    Preprocesamiento de las frases.
    '''
    stemmer = SnowballStemmer('english')

    resultado = []
    for token in gensim.utils.simple_preprocess(txt):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            resultado.append(stemmer.stem(token))

    return resultado


def preprocessingPhrases(txt):
    '''
    Traducimos el texto.
    Dividimoss el texto en frases.
    Eliminamos variabilidad para conseguir palabras con más significado.
    '''
    # Traducimos el texto a inglés
    detect = detectLanguage(txt)
    if detect != 'en':
        txt = translateLanguage(txt, 'en')

    # Dividimos el texto en frases
    frases = sent_tokenize(txt)
    frases = pd.DataFrame({
        'Phrases': frases
    })

    frasesprocesadas = frases['Phrases'].map(preprocessing)

    return frasesprocesadas


def createDict(frasesprocesadas):
    '''
    Diccionario con lista de las palabras más usadas.
    '''
    dictionary = gensim.corpora.Dictionary(frasesprocesadas)

    return dictionary


def createCorpus(dictionary, frasesprocesadas):
    dictionary.filter_extremes(no_below=2, no_above=0.9, keep_n=100000)

    corpus = [dictionary.doc2bow(doc) for doc in frasesprocesadas]

    return corpus


def extractThemes(corpus, dictionary):
    '''
    Extrae los principales temas que subyacen en el texto.
    '''
    lda_model = gensim.models.LdaMulticore(
        corpus, num_topics=1, id2word=dictionary, passes=3, workers=2)
    for idx, topic in lda_model.print_topics(-1):
        print('Tema {} \nPalabras: {}\n'.format(idx+1, topic))
