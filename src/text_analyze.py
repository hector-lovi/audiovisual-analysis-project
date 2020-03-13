import spacy
import nltk
from nltk import *
from nltk.corpus import wordnet
from spacy.matcher import matcher
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def textAnalyze(t):
    '''
    Realiza un análisis de sentimiento sobre un texto.
    '''
    s = SentimentIntensityAnalyzer()
    result = s.polarity_scores(t)
    return result
