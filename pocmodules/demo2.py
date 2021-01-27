# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = '漏洞名称'
		self.vulsystem= '涉及系统'
		self.vulsystemintro = '系统介绍'
		self.vulversion = '危害版本'
		self.fofa='搜索引擎语句'
		self.findtime='发现时间'
		self.cveid='cve号'
		self.refer= '参考'
		self.bbb='个人记录'
		self.testisok=True # 是否测试成功

		self.vulpath='' # 危害链接
		self.headers={} # 请求头	
		self.payload='' # 危害数据
		self.flag = 200 # 利用成功标识


	def c2Func(self,target):
		status=0
		returnData=''

		# 1、处理目标格式
		if target.startswith(('http://','https://')):
			target=target+'/'
			target=target[:target.find('/',8)] #
		else:
			target='https://'+target
		try:
			# 2、准备攻击所需的数据
			url=target.strip('/')+self.vulpath
			# 3、开始攻击
			resp=requests.post(url=url,data=self.payload,headers=self.headers,verify=False,timeout=30)
			# 4、检测是否存在成功标识
			if self.flag == resp.status_code:
				status=1
				returnData='%s is vuln(%s) , vulpath: %s'\
				''%(target.strip('/'),self.vulname,url)
		except Exception as e:
			returnData=str(e)
		# 5、返回状态与数据
		return status,returnData

if __name__ == '__main__':
	target='http://127.0.0.1/'
	pocObj=c2Class()
	print(pocObj.c2Func(target))