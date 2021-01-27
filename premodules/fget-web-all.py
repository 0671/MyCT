# coding:utf-8
import requests
import re
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.isRelease=True
		self.protocol=('http://','https://')
		self.ok_protocol=('<http://','<https://')
		self.rc_port=re.compile(r'(?<=:)\d{2,5}')
		self.port_web=[80,81,82,83,84,85,86,87,88,89,90,7001,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8096,8097,8098,8443,8888,9001,9080,9090,9999]

	def c2Func(self,target):
		status=0
		returnData=[]

		target=target.strip('/')
		if target.startswith(self.ok_protocol):
			flag,url=self.check(target)
			if flag==1:
				status=1
				returnData.append(url)
		else:
			status=-1
			for i in self.protocol:
				target=target.replace(i,'')
			allports=set(self.port_web)
			if ':' in target:
				host,port=target.split(':')
				allports.add(int(port))
			else:
				host=target
			for i in allports:
				url='<http://%s:%d/'%(host,i)
				returnData.append(url)
		return status,returnData
		
	def check(self,url):
		url=url.strip('<')
		try:
			_t=requests.get(url=url,verify=False,timeout=5)
			return 1,_t.url
		except Exception as e:
			return 0,0
if __name__ == '__main__':
	target="137.135.83.245:443"
	pocObj=c2Class()
	print(pocObj.c2Func(target))