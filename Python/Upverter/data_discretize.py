cum_ser = pd.Series()
cum_std = []

for name, g in time.groupby(bins):
	cum_ser = pd.concat([cum_ser, g], ignore_index=True)
	cum_std.append(cum_ser.std())
	
	
d = pd.read_csv(r'I:\Scripts\Python\Upverter\task_time.csv', index_col=0,
				na_values=0)
data_changed = d.applymap(lambda x: min(x, 3900))	
def transform_row(row):
	row.dropna(inplace=True)
	return (row.sum()-row.max()-row.min()) / (len(row) -2)
time_avg = data_changed.apply(transform_row, axis=1).dropna()

	
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, n_jobs=4)
kmeans.fit(time_avg.values.reshape(-1,1))

plt.scatter(time_avg.values, kmeans.labels_)

time_discrete = pd.DataFrame(time_avg)
time_discrete.rename({0:'time'},axis=1,inplace=True)
time_discrete['level'] = kmeans.labels_

ind = time_discrete[time_discrete['time']==3900].index
time_discrete.loc[ind, 'level'] = 3




from sklearn.metrics import silhouette_score
time_changed = time.drop_duplicates()
time_changed = time_changed[time_changed<3900]
X = time_avg.values.reshape(-1,1)
clusters = 20
sc_scores = []
for i in xrange(3, clusters+1):
	kmeans = KMeans(n_clusters=i)
	kmeans.fit(X)
	sc_score = silhouette_score(X, kmeans.labels_,
								metric='euclidean')
	sc_scores.append(sc_score)

	
time = pd.Series()
for col in d.columns:
	time = pd.concat([time, d[col]], ignore_index=True)
time.dropna(inplace=True)
	
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
	
	


