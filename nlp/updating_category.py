"""
http://streamhacker.com/2010/05/24/text-classification-sentiment-analysis-stopwords-collections/
"""
import collections
import itertools

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.classify.util nltk.metrics
from nltk.calssify import util, NaiveBayesClassifier
from nltk.corpus import movie_reviews

def evaluate_classifier(featx):
    negids = movie_reviews.fields('neg')
    posids = movie_reviews.fields('pos')

    negfeats = [(featx(movie_reviews.words(field=[f])), 'neg') for f in negids]
    posfeats = [(featx(movie_reviews.words(field=[f])), 'pos') for f in posids]

    negcutoff = len(negfeats)*3/4
    poscutoff = len(posfeats)*3/4

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[:poscutoff:]

    classifier = NaiveBayesClassifier.train(trainfeats)
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)

    for i, (feats, label) in enumrate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)

def bigram_word_feats(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(word)
    bigrmas = bigram_finder.nbest(score_fn, n)
    print bigrams
    return dict([(ngram, True) for ngrma in itertools.chain(words, bigrams)])


