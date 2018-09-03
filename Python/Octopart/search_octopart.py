import json
import urllib, urllib2
import time, socket
import sys
import pandas as pd

api_key = 'cc1aaad8'

def search_octopart(apiKey, endpoint='part', query="", start=0, limit=10, includes=(), filters={}):
	if endpoint == 'part':
		url = "http://octopart.com/api/v3/parts/search"
	elif endpoint == 'categories':
		url = "http://octopart.com/api/v3/categories/search"
	else:
		raise KeyError(endpoint + ' is not a defined endpoint')
		
	url += 	'?apikey=' + apiKey
	args = [
			('q', query),
			('start', start),
			('limit', limit)
			]
	
	for include in includes:
		args.append(('include[]', include))
		
	for field in filters:
		args.append(('filter[fields]['+field+'][]', filters[field]))
		
	url += '&' + urllib.urlencode(args)
	
	try:
		data = urllib2.urlopen(url, timeout=60).read()
	except socket.timeout:
		print 'timeout, search again in seconds'
		urllib2.time.sleep(30)
		return search_octopart(apiKey, endpoint, query, start, limit, includes, filters)
		
	urllib2.time.sleep(0.5)
	
	try:
		result = json.loads(data)
	except ValueError:
		return None
		
	return result
	
	
def get_batch(apiKey, uids, endpoint='part'):
	if len(uids) > 20:
		raise ValueError('the amount of uids is up to 20')
		
	if endpoint == 'part':
		url = 'http://octopart.com/api/v3/parts/get_multi?'
	elif endpoint == 'categories':
		url = 'http://octopart.com/api/v3/categories/get_multi'
	else:
		raise KeyError(endpoint + ' is not a defined endpoint')
		
	url += 	'?apikey=' + apiKey
	args = [('uid[]', uid) for uid in uids]
	url += '&' + urllib.urlencode(args)
	
	try:
		data = urllib2.urlopen(url, timeout=30).read()
	except socket.timeout:
		print 'search timeout, try again in seconds'
		time.sleep(30)
		return get_batch(apiKey, uids, endpoint)
		
	time.sleep(0.5)
	
	return json.loads(data)
	
	
def write_parts(f, data, categoryName=None):
	items = [result['item'] for result in data['results']]		
	parts = pd.DataFrame(items)
	if categoryName:
		parts[cat_name] = categoryName
		
	parts.to_csv(f, index=False, mode='a', encoding='utf-8',header=None)
	
	

def convert_List2Dict(lst):
	attr = {}
	for i, suffix in zip(lst, xrange(len(lst))):
		attr[str(suffix)] = i
		
	return attr

	
def extract_part_info(partData):
	hits = partData.get('hits', 0)
	parts = []
	
	if hits > 0:
		for res in partData['results']:
			part = {}
			not_needed = ['redirected_uids', '__class__', 'offers', 'brand']
			for term in not_needed:
				res['item'].pop(term, None)			

			for k in res['item'].keys():
				if isinstance(res['item'][k], basestring):
					part[k] = res['item'][k]
					
				elif isinstance(res['item'][k], list):
					item = convert_List2Dict(res['item'][k])
					for k_item in item.keys():
						part[k+'_'+k_item] = item[k_item]	
						
				elif isinstance(res['item'][k], dict):
					item = res['item'][k]
					for k_item in item.keys():
						part[k+'_'+k_item] = item[k_item]
				
				else:
					part[k] = res['item'][k]						
					
			parts.append(pd.DataFrame(part, index=[part.get('uid', 0)]))		
						
	return parts
	
def get_part_classes:
material = pd.read_excel(r'I:\Scripts\Python\Upverter\Materials.xls')
mpns = material['MPN'].values
task_id = material['task_id'].values
result = []
status = ' '
for key_word, id, i in zip(mpns, task_id, xrange(len(mpns))):
	sys.stdout.write(' ' * len(status) + '\r')
	status = '%s / %s	%s	%s' %(str(i), str(len(mpns)), key_word, id)
	sys.stdout.write(status + '\r')
	
	try:
		part_data = search_octopart(api_key, includes=('category_uids','short_description'),
									query=key_word)
	except UnicodeError:
		part_data = None
	
	if part_data:
		extracted = extract_part_info(part_data)
		for df in extracted:
			df['task_id'] = id
		result.extend(extracted)
	
	if (i%100) == 0:
		pd.concat(result, sort=True).to_excel(r'I:\Scripts\Python\Upverter\Octopart_class.xls')
pd.concat(result, sort=True).to_excel(r'I:\Scripts\Python\Upverter\Octopart_class.xls')
	
	
	
root_uid = '8a1e4714bb3951d9'	
categories_all = []
category_root = get_batch(api_key, [root_uid], endpoint='categories')[root_uid]
category_child_uids = category_root['children_uids']

while len(category_child_uids) > 0:
	uid = category_child_uids.pop()
	category = get_batch(api_key, [uid], endpoint='categories')[uid]
	
	print category['name'], ', acient name:', category['ancestor_names']
	categories_all.append(category)
	category_child_uids.extend(category['children_uids'])
	
f_categories = r'D:\categories.xls'
pd.DataFrame(categories_all).to_excel(f_categories, index=False)	

limit = 10
total = 1000	
f_reuslt = r'D:\all_parts.csv'
headers = pd.DataFrame(columns=['__class__',	
							'brand', 'category_uids', 'manufacturer',
							'mpn', 'octopart_url', 'offers', 'redirected_uids',
							'short_description', 'uid',	'category_name'
						])
headers.to_csv(f_reuslt, index=False)
						
categories = pd.read_excel(f_categories,na_values='[]')
for cat in categories.index:
	if not pd.isna(categories.loc[cat]['children_uids']): continue
	
	print 'searching ' + categories.loc[cat]['name']
	resp = search_octopart(api_key, limit=limit,
							includes=('category_uids','short_description'),
							filters={'category_uids':categories.loc[cat]['uid']})
	
	if not resp: continue
	
	hits = resp.get('hits')
	if hits != None:
		cat_name = categories.loc[cat]['name']
		write_parts(f_reuslt, resp, cat_name)
	
		for i in xrange(hits/limit):
			if (i+1)*limit >= total: break
			
			sys.stdout.writelines('fetching ' + str((i+1)*limit) + '/' + str(hits) + ' parts\r')
			resp = search_octopart(api_key, limit=limit, start=(i+1)*limit,
						includes=('category_uids','short_description'),
						filters={'category_uids':categories.loc[cat]['uid']})
			if not resp: continue
						
			write_parts(f_reuslt, resp, cat_name)
			
	
	sys.stdout.writelines('\r\n')
	

