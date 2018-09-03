cum_ser = pd.Series()
cum_std = []

for name, g in time.groupby(bins):
	cum_ser = pd.concat([cum_ser, g], ignore_index=True)
	cum_std.append(cum_ser.std())
	
	
d = pd.read_csv(r'I:\Scripts\Python\Upverter\task_time.csv', index_col=0)
time = pd.Series()
for col in d.columns:
	time = pd.concat([time, d[col]], ignore_index=True)
time.dropna(inplace=True)
	
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=7, n_jobs=4)
kmeans.fit(time.values.reshape(-1,1))

plt.scatter(time.values, kmeans.labels_)
plt.yticks(xrange(len(kmeans.labels_)))


from sklearn.metrics import silhouette_score
time_changed = time.drop_duplicates()
time_changed = time_changed[time_changed<3900]
X = time_changed.values.reshape(-1,1)
clusters = 20
sc_scores = []
for i in xrange(3, clusters+1):
	kmeans = KMeans(n_clusters=i)
	kmeans.fit(X)
	sc_score = silhouette_score(X, kmeans.labels_,
								metric='euclidean')
	sc_scores.append(sc_score)
	
	
#Elbow method
from scipy.spatial.distance import cdist
clusters = 20
mean_distortions = []
X = time.values.reshape(-1,1)
for i in xrange(2, clusters + 1):
	sys.stdout.write('%d / %d\r' %(i, clusters))
	clusters = max(2, clusters)
	kmeans = KMeans(n_clusters=i)
	kmeans.fit(X)
	centers = kmeans.cluster_centers_
	
	mean_distortions.append(sum(np.min(cdist(X, centers)
							, axis=1))/X.shape[0])
	
