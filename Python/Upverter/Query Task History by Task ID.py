__author__ = 'frank.qiu'

import urllib
import urllib2
import requests
import cookielib
import re
import xml.etree.ElementTree as ET
import datetime
import ssl
import json
	
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
	

def getTasksInfo(taskIDs):
	
	
	
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



