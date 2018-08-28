import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import metrics
import time


def extract_features(data, vectorizer):
	X_train_text, X_test_text, Y_train, Y_test = train_test_split(data['short_description'],
												data['category_name'], test_size=0.25)
												
	if isinstance(vectorizer, HashingVectorizer):
		X_train = vectorizer.transform(X_train_text)
		X_test = vectorizer.transform(X_test_text)
		
	else:
		X_train = vectorizer.fit_transform(X_train_text)
		X_test = vectorizer.transform(X_test_text)
	
	return  X_train, Y_train, X_test, Y_test
	

def benchmark(classifer, vect_features):
	try:
		classifer.fit(*vect_features[:2])
		predict = classifer.predict(vect_features[2])
		return metrics.accuracy_score(vect_features[-1], predict)
		
	except Exception as e:
		return e
	
	

data = pd.read_csv(r'D:\top_parts.csv')
data.dropna(inplace=True)
data['manuf_desc'] = data['manufacturer'].str.replace(' ', '_').\
					str.cat(data['short_description'], sep=' ')

vects = {'Tfid': TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english'),
		'Hash': HashingVectorizer(stop_words='english'),
		'Count': CountVectorizer()}
		
clfs = {'naive_bayes': MultinomialNB(),
		'linear_SVC': LinearSVC(loss='hinge', penalty='l2'),
		'SGD': SGDClassifier(loss='hinge', penalty='l2'),
		'randdom_frost': RandomForestClassifier(n_estimators=100)}
		

for v in vects.keys():
	features = extract_features(data, vects[v])
	
	for c in clfs.keys():
		if (c=='naive_bayes') and (v=='Hash'): continue
		
		t0 = time.time()
		s = benchmark(clfs[c], features)
		duration = time.time()-t0
		
		if isinstance(s, float):
			print 'vector: %s, classfier: %s, accuracy: %0.2f, time: %f' %(v, c, s, duration)
		else:
			print 'vector: %s, classfier: %s, accuracy: %s' %(v, c, s)
		