# coding:utf-8
import requests
import re

requests.packages.urllib3.disable_warnings()



class c2Class(object):
	def __init__(self):
		self.headers={
			'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:56.0) Gecko/20100101 Firefox/56.0',
			'Connection':'close'}
		self.rc_title=re.compile(r'(?<=<title>|<TITLE>)[\s\S]+?(?=</title>|</TITLE>)')
		# 抓取标题的正则表达式列表
		self.rc_retry=[
		re.compile(r'(?<=<meta http-equiv="refresh" content="0; URL=)[\s\S]+?(?=" />)'),
		re.compile(r'(?<=[window|document]\.location\.href=")[\s\S]+?(?=")'),
		re.compile(r'(?<=window.open\(")[\s\S]+?(?=")'),
		re.compile(r'(?<=<META HTTP-EQUIV="REFRESH" CONTENT="\d; URL=/)[\s\S]+?(?=")'),
		]
		self.rc_exception_name=re.compile(r"(?<=')[\s\S]+?(?=')")

	def c2Func(self,target):
		status =0
		if target.startswith('http://') or target.startswith('https://'):
			if ':443' in target:
				target=target.replace('http://','https://').replace(':443','')
			try:
				# time.sleep(0.1)
				resp=requests.get(url=target,headers=self.headers,verify=False,timeout=3)
				if resp.encoding=='ISO-8859-1':
					resp.encoding='utf-8'
				text=resp.text
				# print(text)
				url=''
				title=self.rc_title.search(text)
				if title==None:
					for ri in self.rc_retry:
						_path=ri.search(text)
						if _path!=None:
							path=_path.group()
							if not path.startswith('/'):
								path='/'+path
							url=target+path
							status=-1
							returnData=[url]
							return status,returnData
					returnData=target+''
					status=1
					return status,returnData			
				else:
					title=title.group()
				# print(title)
				if title !=None:
					try:
						# windows平台下使用下一行代码,因为windows的cmd的默认编码格式是gbk（963）编码,所以需要对标题进行编码
						returnData=target+":"+title.encode('gbk','ignore').strip()
						# unix平台下使用下一行代码，因为unix平台的bash的默认编码格式一般为utf-8
						# returnData=target+":"+title.strip()
					except UnicodeDecodeError as e:
						returnData=target+":"+title.strip()
					except TypeError as e:	
						returnData=target+":"+title.strip()
					# 避免windows下控制台输出时，报错
					# UnicodeEncodeError: ‘gbk’ codec can’t encode character u’\u200e’ in position 43: illegal multibyte sequence
					# 报错的意思说，utf8的有些编码，gbk无法识别
					# 通过添加ignore来忽略非法的字符，如： encode('gbk','ignore')
					status=1
				else:
					pass
			except Exception as e:
				status=1
				target='Err_Do:'+target
				# print(str(e.__class__))
				# print(e)
				returnData=target+'|'+self.rc_exception_name.search(str(e.__class__)).group()
		else:
			returnData=[]
			returnData.append('http://'+target)
			# returnData.append('https://'+target)
			status=-1
		return status,returnData

if __name__ == '__main__':
	target="http://192.168.3.12:8080/"
	pocObj=c2Class()
	print(pocObj.c2Func(target))

