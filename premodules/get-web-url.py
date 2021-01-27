# coding:utf-8
import requests
import sys
requests.packages.urllib3.disable_warnings()



class c2Class(object):
	def __init__(self):
		self.isRelease=True
		self.protocol=('http://','https://')
		self.port=[81,82,83,84,85,86,87,88,89,90,7001,8080,8081,8082,8083,8084,8085,8086,8087,8088,8089,8090,8091,8092,8093,8094,8095,8096,8097,8098,8443,8888,9001,9080,9090,9999]

	def c2Func(self,target):
		status=0
		returnData=[]

		if target.startswith(self.protocol):
			flag,url=self.check(target)
			# flag,url=self.check_special(target)
			if flag==1:
				status=1
				returnData.append(url)
		else:
			status=-1
			if ":" in target:# 针对fofa搜索出来的结果 like 111.230.116.47:8090
				for ptl in self.protocol:
					url=ptl+target+'/' # http://111.230.116.47:8090/
					returnData.append(url)
				target=target[:target.find(':')] # 111.230.116.47
			for ptl in self.protocol:
				url=ptl+target+'/'
				returnData.append(url)
				for p in self.port:
					url=ptl+target+':'+str(p)+'/'
					returnData.append(url)
		return status,returnData
		
	def check(self,url):
		try:
			_t=requests.get(url=url,verify=False,timeout=3)
			return 1,_t.url
		except Exception as e:
			# print(e)
			return 0,0
	def check_special(self,url,special='JumpServer'): # 获取含有特殊字符在网页中的位置
		try:
			# print(url)
			_t=requests.get(url=url,verify=False,allow_redirects=False,timeout=3)
			if sys.version[0]=='3':
				_ts=str(_t.content,'utf-8') #  py3写法，因为py3字符串变量全部默认都是bytes类型，所以需要转换
			elif sys.version[0]=='2':
				_ts=_t.content # py2写法，
			if special in _ts:
				# print(_t.content)
				return 1,_t.url
			else:
				return 0,0
		except Exception as e:
			return 0,0
if __name__ == '__main__':
	target="http://119.84.148.218:8090/"
	pocObj=c2Class()
	print(pocObj.c2Func(target))