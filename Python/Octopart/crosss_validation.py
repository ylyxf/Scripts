import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.svm import LinearSVC
from sklearn import metrics
import numpy.random as rand

def corss_validation(data, X, Y, test_size=0.2):
	data = data.loc[rand.permutation(data.index)]
	
	splited_data = []
	for i in xrange(int(1 / test_size)):
		test = data.loc[data.index[int(i*test_size*len(data)):int((i+1)*test_size*len(data))]]
		train = data.drop(test.index)
		
		X_train = train[X]
		X_test = test[X]
		Y_train = train[Y]
		Y_test = test[Y]
		
		splited_data.append((X_train, X_test, Y_train, Y_test))
		
	return splited_data
	

def vectorizer_features(data_test, vectorizer):
	if isinstance(vectorizer, HashingVectorizer):
			X_train = vectorizer.transform(data_test[0])
			X_test = vectorizer.transform(data_test[1])
			
	else:
		X_train = vectorizer.fit_transform(data_test[0])
		X_test = vectorizer.transform(data_test[1])
			
	Y_train = data_test[2]
	Y_test = data_test[3]
		
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
									

vector = HashingVectorizer(stop_words='english')
clf = LinearSVC(loss='hinge', penalty='l2')

									
scores = []
for d in corss_validation(data, 'short_description', 'category_name'):
	features = vectorizer_features(d, vector)
	score = benchmark(clf, features)
	if isinstance(score, float):
		scores.append(score)
		
if len(scores) > 0:
	s = 0
	for i in scores:
		s += i
	print 'average accuracy: %3f' %(s/len(scores))
	
else:
	print 'something wrong'
	

	
	