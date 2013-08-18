import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews

def evaluate_classifier(featx):
    negids = movie_reviews.fielids('neg')
    posids = movie_reviews.fielids('pos')

    negfeats = []
