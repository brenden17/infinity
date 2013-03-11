import nltk
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

finder = BigramCollocationFinder.from_web(nltk.corpus.genesis.words('english-web.txt'))

print finder.nbest(bigram_measures.pmi, 10)
