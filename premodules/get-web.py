# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()



class c2Class(object):
	def __init__(self):
		self.isRelease=True
		self.protocol=('http://','https://')
		self.port_web=[80,81,82,83,84,85,86,87,88,89,90,443,7001,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8096,8097,8098,9080,9090]

	def c2Func(self,target):
		status=0
		returnData=[]

		if target.startswith(self.protocol):
			if self.check(target)==1:
				status=1
				returnData.append(target)
		else:
			status=-1
			for p in self.port_web:
				for ptl in self.protocol:
					url=ptl+target+':'+str(p)+'/'
					returnData.append(url)
		return status,returnData
		
	def check(self,url):
		try:
			_t=requests.get(url=url,verify=False,timeout=2)
			return 1
		except Exception as e:
			return 0
if __name__ == '__main__':
	target="192.168.3.12"
	pocObj=c2Class()
	print(pocObj.c2Func(target))