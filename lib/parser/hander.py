#coding:utf-8
import os
import argparse
from lib.core.log import DEBUG
from lib.core.setting import API_KEY
from lib.core.data import paths


# 并发数是否在一定范围
def concuNum(_str):
	num=int(_str)
	if num > 9999 or num <= 0:
		errMsg="Concurrent number must be in the range of [1,9999], '%s' does not meet"%num
		raise argparse.ArgumentTypeError(errMsg)
	return num

# 检测处理模块文件是否存在
def fileNameOfPocM(_str):
	_fn=str(_str)
	# 修正文件名
	fileName=_fn+('' if  _fn.lower().endswith('py') else '.py')
	filePath=paths['POCMODULE_PATH']
	return isFile(fileName,filePath)

# 检测预处理模块文件是否存在
def fileNameOfPreM(_str):
	_fn=str(_str)
	fileName=_fn+('' if  _fn.lower().endswith('py') else '.py')
	filePath=paths['PREMODULE_PATH']
	return isFile(fileName,filePath)

# 检测并发目标文件是否存在
def fileNameOfTgt(_str):
	fileName=str(_str)
	filePath=paths['ROOT_PATH']
	return isFile(fileName,filePath)

# 检测文件是否真实存在于指定路径下
def isFile(fn,fp):
	fullPath=os.path.join(fp,fn)
	if not os.path.isfile(fullPath):
		errMsg="Cannot find the file named '%s' under %s"%(fn,fp)
		raise argparse.ArgumentTypeError(errMsg)
	return fullPath

# 检测Fofa api是否可用
def testFofa(_str):
	query=_str
	email=API_KEY['Fofa']['email']
	key=API_KEY['Fofa']['key']
	url="https://fofa.so/api/v1/info/my?email=%s&key=%s"%(email,key)
	import requests,json
	resp=requests.get(url)
	authData=json.loads(resp.content)
	if 'error' in authData:
		errMsg="FOFA API is not available. Please check the FOFA configuration(email,key) located in lib/code/setting.py"%(fn,fp)
		raise argparse.ArgumentTypeError(errMsg)
	if authData['isvip'] == False and authData['fcoin']==0:
		errMsg="FOFA API is not available. Because you are no VIP users and FOFA coin is not enough!"
		raise argparse.ArgumentTypeError(errMsg)
	return query

# 自定义一个Action类
# 自定义 action 方法需要继承自 argparse.Action 类,并且实现一个 __call__ 方法
# myActionDebug继承自argparse._StoreTrueAction
class myActionDebug(argparse._StoreTrueAction):
	def __call__(self, parser, namespace, values, option_string=None):
		# 如果参数使用了该Action，会自动调用__call__方法，从而调用DEBUG函数
		setattr(namespace,self.dest,True)
		DEBUG()
