# coding:utf-8
import requests
import threading
import Queue
requests.packages.urllib3.disable_warnings()


class c2Class(object):
	def __init__(self):
		self.protocol='http://'
		self.port_wlg=7001

	def c2Func(self,target):
		status=0
		returnData=[]

		if target.startswith(self.protocol):
			if self.check(target)==1:
				status=1
				returnData.append(target)
		else:
			status=-1
			url=self.protocol+target+':'+str(self.port_wlg)+'/'
			returnData.append(url)
		return status,returnData

	def check(self,url):
		try:
			_t=requests.get(url=url,verify=False,timeout=2)
			return 1
		except Exception as e:
			return 0
if __name__ == '__main__':
	target="127.0.0.1"
	target1="http://127.0.0.1:7001/"
	pocObj=c2Class()
	print(pocObj.c2Func(target))
	print(pocObj.c2Func(target1))