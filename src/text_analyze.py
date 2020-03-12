import spacy
import nltk
from nltk import *
from nltk.corpus import wordnet
from spacy.matcher import matcher
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def textAnalyze(text):
    '''
    Realiza un análisis de sentimiento sobre un texto.
    '''
    s = SentimentIntensityAnalyzer()
    result = s.polarity_scores(text)
    print(result)


textAnalyze('mírate preparada para comerte el día y cuidándote con Alpro avena 100% vegetal bien hecho con deliciosa buena fuente de calcio y fibra sin nada de azúcar y por supuesto sin edulcorantes un poco más porque no Alpro 100% vegetal bien hecho')
