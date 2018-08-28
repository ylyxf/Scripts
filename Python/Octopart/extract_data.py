import pandas as pd
import numpy.random as rand

def get_top(data, limit):
	
	return data.loc[rand.permutation(data.index)[:limit]]
	
	
parts = pd.read_csv(r'D:\all_parts.csv', usecols=['category_name',
												'manufacturer', 'mpn', 
												'short_description'])
											
	
parts_by_cats = parts.groupby(lambda x: parts['category_name'].loc[x])
parts_top = parts_by_cats.apply(get_top, limit=500)

manuf_match = r"u'name': u'(.+)'"	
parts_top['manufacturer'] = parts_top['manufacturer'].str.extract(manuf_match)[0].values

parts_top.to_csv(r'D:\top_parts.csv')
#cat_match = r'\[(\w*),'
#parts_top['category_uids'] = parts_top['category_uids'].str.extract(cat_match)[0].values

#categories = pd.read_excel(r'D:\categories.xls', index_col=7)
#cat_uids = categories['name'].to_dict()
#parts_top['category_name'] = [cat_uids.get(i) for i in parts_top['category_uids']]

