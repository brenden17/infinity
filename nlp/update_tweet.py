"""
source from :
www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
"""
from nltk import FreqDist
from nltk import classify
from nltk import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords

pos_tweet = [('I love this car', 'positive'),
                ('This view is amazing', 'positive'),
                ('I feel greate this morning', 'positive'),
                ('I am so excited about the concert', 'positive'),
                ('He is my best friend', 'positive')]

neg_tweet = [('I do not like this car', 'negative'),
                ('this view is borrible', 'negative'),
                ('I feel tired this morning', 'negative'),
                ('I am not looking forward to the concert', 'negative'),
                ('He is my enemy', 'negative') ]

tweet = []
lemmatizer = WordNetLemmatizer()
stopset = stopwords.words('english')
stemmer = PorterStemmer()

def normalize(sentence, stopword=False, stem=False, lemma=True):
    words = word_tokenize(sentence)
    if stopword:
        word = [word for word in words if not word in stopset] 
    if stem:
        words = [stemmer.stem(word) for word in words]
    if lemma:
        words = [lemmatizer.lemmatize(word, 'v') for word in words]
    return words

for (words, sentiment) in pos_tweet + neg_tweet:
    s = normalize(words)
    tweet.append((s, sentiment))

def get_words_in_tweets(tweet):
    all_words = []
    for words, sentiment in tweet:
        all_words.extend(words)
    return all_words

def get_words_features(wordlist):
    wordlist = FreqDist(wordlist)
    return wordlist.keys()

word_features = get_words_features(get_words_in_tweets(tweet))

#print word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

training_set = classify.apply_features(extract_features, tweet) 
#print training_set

classifier = NaiveBayesClassifier.train(training_set)
#print classifier.show_most_informative_features(32)
print classify.accuracy(classifier, training_set)

t = 'Larry is not my friend'
print  classifier.classify(extract_features(t.split()))
