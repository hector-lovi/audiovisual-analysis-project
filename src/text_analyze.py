import spacy
import nltk
from nltk import *
import es_core_news_sm
from collections import Counter
from nltk.corpus import wordnet
from spacy.matcher import matcher
from spacy.lang.es import Spanish
from nltk.corpus import wordnet
from spacy.matcher import matcher
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def textSentiment(txt):
    '''
    Realiza un análisis de sentimiento sobre un texto.
    '''
    s = SentimentIntensityAnalyzer()
    result = s.polarity_scores(txt)
    return result


def textAnalysis(txt):
    '''
    Realiza un nálisis textual.
    '''
    nlp = es_core_news_sm.load()

    complete_doc = nlp(txt)
    words = [
        token.txt for token in complete_doc if not token.is_stop and not token.is_punct]

    word_freq = Counter(words)
    common_words = word_freq.most_common(5)

    nouns = []
    adjectives = []

    for token in complete_doc:
        print(token, '-', token.tag_, token.pos_)

    for token in complete_doc:
        if token.pos_ == 'NOUN':
            nouns.append(token)
        if token.pos_ == 'ADJ':
            adjectives.append(token)

    print('\nPALABRAS REPETIDAS...')
    print(common_words)
    print('\nNOMBRES...')
    print(nouns)
    print('\nADJETIVOS...')
    print(adjectives)
