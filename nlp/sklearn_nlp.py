from sklearn.feature_extraction.text import CountVectorizer
"""
CountVectorizer is based on bag of words
"""
vectorizer = CountVectorizer(min_df=1)

corpus = ['This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',]

X = vectorizer.fit_transform(corpus)
print vectorizer.get_feature_names()
print X.toarray()

analyze = vectorizer.build_analyzer()
print analyze("This is a text document to analyze")

print vectorizer.transform("This is a text document to analyze").toarray()


"""
TfidfTransformer is based on tf-idf
"""
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()
print transformer
counts = [[3, 0, 1],
            [2, 0, 0],
            [3, 0, 0],
            [4, 0, 0],
            [3, 2, 0],
            [3, 0, 2]]

#tfidf = transformer.fit_transform(counts)
tfidf = transformer.fit_transform(X.toarray())
print tfidf.toarray()
