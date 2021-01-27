# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.isRelease=True
		self.protocol=('http://','https://')

	def c2Func(self,target):
		status=0
		returnData=[]

		if target.startswith(self.protocol):
			flag,url=self.check(target)
			if flag==1:
				status=1
				returnData.append(url)
		else:
			status=-1
			url='http://'+target+'/'
			returnData.append(url)
			if ':443' not in target:
				url='https://'+target+'/'
				returnData.append(url)
		return status,returnData
		
	def check(self,url):
		try:
			_t=requests.get(url=url,verify=False,timeout=5)
			return 1,_t.url
		except Exception as e:
			return 0,0
if __name__ == '__main__':
	target="137.135.83.245:443"
	pocObj=c2Class()
	print(pocObj.c2Func(target))