__author__ = 'frank.qiu'

import urllib, urllib2
import requests
import cookielib
import re
import xml.etree.ElementTree as ET
import datetime
import ssl
import json
import pandas as pd
import sys
	
def upverterLogin(userName, password, site='mainSite'):
	loginPageUrl = 'https://upverter.com/login/'
	enteranceUrl = {'mainSite': "https://upverter.com/login/",
				'forum': 'https://forum.upverter.com/session/sso?return_path=%2F'
				}.get(site)
				
	if enteranceUrl == None:
		raise KeyError
	
	cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
	
	loginPage = opener.open(loginPageUrl)
	csrfToken = re.search(r'<meta content="(.+)" name=',loginPage.read()).group(1)
	postData = urllib.urlencode({'_csrf_token':csrfToken,
                                 'login_username':userName,
                                 'login_password':password,
                                 'type':'upverter',
                                 'next':'%2F'})
								 	
	if site == 'forum':
		enteranceUrl = opener.open(enteranceUrl).geturl()
		
	req = urllib2.Request(enteranceUrl, postData)
	connLogin = opener.open(req)
		
	
	return opener
	
	
def searchUpverterForum(content, opener=None):
	searchUrl = 'http://forum.upverter.com/search?'
	searchUrl += urllib.urlencode({'q' : content})
	
	header = {
				'Accept': 'application/json, text/javascript, */*; q=0.01',
				'X-Requested-With':	'XMLHttpRequest'
			}
	req = urllib2.Request(searchUrl, headers=header)
	
	if opener == None:
		resp = urllib2.urlopen(req)
	else:
		resp = opener.open(req)
		
	return resp
	
	

def parseHistory(taskHistoryPage):
    rawHistory = re.search(r'<tbody>((?:.|\n)*?)</tbody>',taskHistoryPage).group(0)
	print rawHistory

    eleHistory = ET.fromstring(rawHistory)

    historyList = []
    for rowEle in eleHistory.iter("tr"):
        dataList = []
        for colEle in rowEle.iter("td"):
            dataList.append(colEle.text)

        historyList.append(dataList)

    historyDict = {}
    for task in reversed(historyList):
        if task[2] == "component_task.created_component":
            if not historyDict.has_key(task[1]):
                historyDict[task[1]] = {'end':task[0]}

            elif not historyDict[task[1]].has_key('start'):
                historyDict[task[1]]['end'] = task[0]

            else:continue

        if task[2] == 'assigned' and historyDict.has_key(task[1]):
            if not historyDict[task[1]].has_key('start'):
                historyDict[task[1]]['start'] = task[0]

    validHistoryDict = {}
    for user in historyDict:
        if user == "None" : continue

        if historyDict[user].has_key("start") and historyDict[user].has_key("end"):
            historyDict[user]["duration"] =(datetime.datetime.strptime(historyDict[user]["end"],"%Y-%m-%d %H:%M") -
                                 datetime.datetime.strptime(historyDict[user]["start"],"%Y-%m-%d %H:%M")).total_seconds()

            validHistoryDict[user] = historyDict[user]

    return validHistoryDict


def fetchTaskHistory(taskId, opener):
	histUrl = "https://upverter.com/task/%s/debug/" %(taskId)

	try:
		resp = opener.open(histUrl)
		history = parseHistory(resp.read())
		
		return history
		
	except urllib2.HTTPError:
		return None
	
	
def fetchMPNbyTaskId(taskId, opener):
	resp = searchUpverterForum(taskId, opener)
	data = json.loads(resp.read())
	
	if data.get('topics'):
		mpn = data['topics'][0].get('title').split(' -- ')[0]
		posts = data['topics'][0]['posts_count']
	
		return (mpn, posts)
		
	else:	
		return None
		
def fetchPartClass(componentId):
	partUrl = 'https://upverter.com/upn/revision/' + componentId
	pattern = r'<div class="col"><div> Device Class L2</div></div>\s+<div class="col"><div>(.+)</div></div>'
   
	try:
		data = urllib2.urlopen(partUrl).read()
		classL2 = re.search(pattern, data).group(1)
		
		return classL2
		
	except:
		return None
	

def getTasksInfo():
	result = r'materials.csv'
	data = pd.read_csv(r'task_history__component_id.csv', index_col='task_id',
						parse_dates=['ts'])
						
	counts = {
			  'assigned' : pd.read_csv(r'task_history__assigned.csv', index_col='task_id'),
			  'rejected' : pd.read_csv(r'task_history__rejected.csv', index_col='task_id'),
			  'skipped' : pd.read_csv(r'task_history__skipped.csv', index_col='task_id')
			  }
			  
	for d in counts.keys():
		data = data.join(counts[d], rsuffix='_'+d, how='left')
	data.rename({'count':'count_assigned'}, axis=1, inplace=True)
	data.drop(data[pd.isna(data.count_assigned)].index, inplace=True)

	factors = {
				'complexity': pd.read_csv('task_history__complexity_factors.csv'),
				'footprints': pd.read_csv(r'task_history__footprint_primitives.csv'),
				'manufacturers': pd.read_csv(r'task_history__manufacturers.csv')
			   }
	for d in factors.keys():
		data = data.join(factors[d].set_index('component_id'),
						on='component_id', how='inner')
	data.rename({'sum':'primitives'}, axis=1, inplace=True)
	data.drop('factors__component_id', axis=1, inplace=True)
		
	requester = upverterLogin('frank.qiu', '123456',site='forum')
	data['MPN'] = pd.np.NaN
	data['posts'] = pd.np.NaN
	data['class_L2'] = pd.np.NaN

	for task_id,i in zip(data.index, xrange(len(data))):
		sys.stdout.write('%s / %s\r' %(str(i+1), str(len(data))))

		cmp_id = data['component_id'].loc[task_id]
		try:
			data.MPN, data.posts = fetchMPNbyTaskId(task_id, requester) 
			data.class_L2 = fetchPartClass(cmp_id)
			
		except:
			data.to_csv(result)
			print '\r\n' + task_id + ' is with something  wrong'
			
	data.to_csv(result)

def main():
	taskIDList = ['02a7d26767e79a7b',
	'03133fbe0622831c',
	]

	#remove duplicated task id
	TaskIdDict = {}
	for taskID in taskIDList:
		TaskIdDict[taskID] = taskID
	taskIDList = TaskIdDict.keys()


	print "login in Upverter"
	requester = upverterLogin("frank.qiu","123456")

	print "taskID", "user", "duration", "taskTimeAeverage", "taskTimeMin", "start"

	taskReport = open("report.txt", "wb")
	for taskID in taskIDList:
		response = requester.open("https://upverter.com/task/" + taskID + "/debug/")
		taskHistoryPage = response.read()

		userHistory = parseHistory(taskHistoryPage)

		taskTimeAeverage = 0
		taskTimeMin = 9999
		taskTimeTotal = 0
		for user in userHistory:
			if not userHistory[user].has_key("duration"):continue

			taskTimeTotal = taskTimeTotal + userHistory[user]["duration"]

			if userHistory[user]["duration"] < taskTimeMin:
				taskTimeMin = userHistory[user]["duration"]

		taskTimeAeverage = taskTimeTotal / len(userHistory)

		for user in userHistory:
			if not userHistory[user].has_key("duration"):continue
			print taskID, user, str(userHistory[user]["duration"] / 60), str(round(taskTimeAeverage /60) ), \
				str (taskTimeMin / 60), userHistory[user]["start"]
			taskReport.write(taskID +"^" +
							 user + "^" +
							 str(userHistory[user]["duration"] / 60) + "^"+
							 str(round(taskTimeAeverage /60) ) + "^"+
							 str (taskTimeMin / 60) + "^" +
							 userHistory[user]["start"] + "\r\n")

	taskReport.close()
	print "done"

	
if __name__ == "__mian__":
	main()



