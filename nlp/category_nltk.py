#source
#-http://nltk.org/_modules/nltk/classify/naivebayes.html
#

"""
category by name
"""
def category_by_name():
    from nltk import NaiveBayesClassifier
    from nltk import classify
    from nltk.corpus import names
    from nltk.classify import apply_features
    import random

    names = ([(name, 'male') for name in names.words('male.txt')] +[(name, 'female') for name in
    names.words('female.txt')])

    random.shuffle(names)

    def gender_features(word):
        return {'last_letter':word[-1]}

    train_set = apply_features(gender_features, names[500:])
    test_set = apply_features(gender_features, names[:500])

    classifier = NaiveBayesClassifier.train(train_set)
    print classifier.classify(gender_features('Neo')) 
    print classify.accuracy(classifier, train_set)

"""
categories by neg, pos
"""
def category_by_movie():
    from nltk.corpus import movie_reviews as mr
    from nltk import FreqDist
    from nltk import NaiveBayesClassifier
    from nltk import classify
    from nltk.corpus import names
    from nltk.classify import apply_features
    import random

    documents = [(list(mr.words(f)), c) for c in mr.categories() for f in
mr.fileids(c)]
    random.shuffle(documents)

    all_words = FreqDist(w.lower() for w in mr.words())
    word_features = all_words.keys()[:2000]

    def document_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    #print document_features(mr.words('pos/cv957_8737.txt'))
    #print documents[0]

    features = [(document_features(d), c) for (d, c) in documents]
    train_set, test_set = features[100:], features[:100]
    classifier = NaiveBayesClassifier.train(train_set)
    print classify.accuracy(classifier, train_set)

"""
POS with decision tree
"""
def category_by_pos():
    from nltk.corpus import brown
    from nltk import FreqDist
    from nltk import DecisionTreeClassifier
    from nltk import NaiveBayesClassifier
    from nltk import classify

    suffix_fdist = FreqDist()
    for word in brown.words():
        word = word.lower()
        suffix_fdist.inc(word[-1:])
        suffix_fdist.inc(word[-2:])
        suffix_fdist.inc(word[-3:])

    common_suffixes = suffix_fdist.keys()[:100]
#    print common_suffixes

    def pos_features(word):
        features = {}
        for suffix in common_suffixes:
            features['endswith(%s)' % suffix] = word.lower().endswith(suffix)
        return features

    tagged_words = brown.tagged_words(categories='news')
    featuresets = [(pos_features(n), g) for (n, g) in tagged_words]
    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
#    classifier = DecisionTreeClassifier.train(train_set)
#    print 'Decision Tree %f' % classify.accuracy(classifier, test_set)

    classifier = NaiveBayesClassifier.train(train_set)
    print 'NaiveBay %f' % classify.accuracy(classifier, test_set)

def update_category_by_pos():
    from nltk.corpus import brown
    from nltk import NaiveBayesClassifier
    from nltk import classify
    from nltk.tag import untag
    from nltk import DecisionTreeClassifier

    def pos_features(sentence, i):
        features = {'suffix(1)':sentence[i][-1:],
                    'suffix(2)':sentence[i][-2:],
                    'suffix(3)':sentence[i][-3:]
                    }
        features['prev-word'] = '<start>' if i==0 else sentence[i-1]
        return features

    print pos_features(brown.sents()[0], 8)

    tagged_sents = brown.tagged_sents(categories='news')
    featuresets = []

    for tagged_sent in tagged_sents:
        untagged_sent = untag(tagged_sent)
        for i, (word, tag) in enumerate(tagged_sent):
            featuresets.append((pos_features(untagged_sent, i), tag))

    size = int(len(featuresets) * 0.1)
    train_set, test_set = featuresets[size:], featuresets[:size]
#    classifier = NaiveBayesClassifier.train(train_set)
    classifier = DecisionTreeClassifier.train(train_set)
    print 'NaiveBay %f' % classify.accuracy(classifier, test_set)

if __name__ == '__main__':
   update_category_by_pos() 
