# coding:utf-8

import threading
import os
import re
import sys
import logging
from lib.core.data import paths,conf,logger,runtime,args
from lib.core.static import CUSTOM_LOGGING,ENGINE_MODE
from lib.core.log import cmd_hd
from lib.core.setting import IS_WIN,RELATIVE_PATH,BANNER,ISCALLGRAPH
from thirdparty.colorama.initialise import init as winColorInit
from thirdparty.termcolor import colored
from thirdparty.utils import traceFunc


# Set various paths of MyCT
def setPaths():
	# Set path
	root_path=fileUpN(os.path.realpath(__file__),3)
	paths['ROOT_PATH']=root_path
	paths['POCMODULE_PATH']=os.path.join(root_path,RELATIVE_PATH['POCMODULE'])
	paths['PREMODULE_PATH']=os.path.join(root_path,RELATIVE_PATH['PREMODULE'])
	paths['OUTPUT_PATH']=os.path.join(root_path,RELATIVE_PATH['OUTPUT'])
	paths['DATA_PATH']=os.path.join(root_path,RELATIVE_PATH['DATA'])
	# If there is no corresponding directory, generate
	if not os.path.exists(paths['POCMODULE_PATH']):
		os.mkdir(paths['POCMODULE_PATH'])
	if not os.path.exists(paths['OUTPUT_PATH']):
		os.mkdir(paths['OUTPUT_PATH'])
	if not os.path.exists(paths['DATA_PATH']):
		os.mkdir(paths['DATA_PATH'])
	if not os.path.exists(paths['PREMODULE_PATH']):
		os.mkdir(paths['PREMODULE_PATH'])

	logger.log(CUSTOM_LOGGING.SUCCESS,'Set the program path successfully')

# 返回文件fn向上n层的目录
def fileUpN(fn,n=1):
	while n >0:
		d=os.path.dirname(fn)
		n-=1
		fn=d 
	return d

# If MyCT is running under windows, perform the initialization of the 'colorama' library, so that the windows console supports ANSI escape sequences-that is, colorful sequences
def initWinStdout():
	if IS_WIN:
		winColorInit()
	logger.log(CUSTOM_LOGGING.SUCCESS,'Initialize color output completed')

# Print banner information
def printBanner():
	_=BANNER
	if not getattr(cmd_hd,'is_tty',False): # 如果cmd_hd没有is_tty标识(终端标识)，则删除BANNER中的ANSI转义序列再打印
		_=re.sub(r"\033.+?m","",_)
	print(_)

# 调用方：MyCT\lib\core\config.py
# 返回列表中value相关的信息:数量,以及符合flag对应的对比函数的元素的最后位置
# flag可以为:0,1,2,3。其中，0代表小于 1代表等于 2代表大于 3代表不等于
def ValueInfoInList(l,value,flag=1): 
	def _lt(a,b): # less than 
		return a<b
	def _eq(a,b): # equal to
		return a==b
	def _gt(a,b): # greater than
		return a>b
	def _ne(a,b): # not equal to
		return a!=b
	funcList=[_lt,_eq,_gt,_ne]
	compare=funcList[flag] # 根据flag选择对比函数
	num=0
	index=-1
	for i in range(len(l)):
		if compare(l[i],value):
			index=i
			num+=1
	return (num,index)

# Returns a generator that generates int numbers between 'start' and 'end'
def intRange(start,end):
	if start > end:
		errMsg="The starting number needs < the ending, but %s > %s"%(start,end)
		raise ValueError(errMsg)
	while start <= end:
		yield start
		start+=1

# 装饰器函数，使得每次线程模式下，能在锁保护下去操作全局变量
def threadLock(lock):
	def middle(func):
		def wrapper(*args,**kwargs):
			if runtime['engineMode']==ENGINE_MODE.THREAD:
				lock.acquire()
			result=func(*args,**kwargs)
			if runtime['engineMode']==ENGINE_MODE.THREAD:
				lock.release()
			return result
		return wrapper
	return middle


# 装饰器函数，生成装饰函数的函数调用图
def callGraph(func):
	flag=0
	try:
		from pycallgraph import PyCallGraph
		from pycallgraph.output import GraphvizOutput
		from pycallgraph import Config
		from pycallgraph import GlobbingFilter
		flag=1
	except Exception as e:
		pass
	def callgraphwrapper(*args,**kwargs):
		if flag==1 and ISCALLGRAPH:
			config = Config()
			config.trace_filter = GlobbingFilter(exclude=[
				'thirdparty.*'
			])
			graphviz = GraphvizOutput()
			graphviz.output_file = 'docx/callGraph.png'
			
			with PyCallGraph(output=graphviz,config=config):
				result=func(*args,**kwargs)
		else:
			result=func(*args,**kwargs)
		return result
	return callgraphwrapper

# 装饰器函数，调试模式下会弹出装饰函数的调用堆栈图
def callStack(func):
	def callstackwrapper(*args,**kwargs):
		if runtime['debug']==True and ISCALLGRAPH:
			traceFunc()
		result=func(*args,**kwargs)
		return result
	return callstackwrapper

# MyCT专属print函数,避免线程模式下logging与标准输出形成死锁
def printToStdout(data,color=None,on_color=None,bold=False):
	if bold:
		msg= colored(text=data, color=color, on_color=on_color, attrs=['bold'])
	else:
		msg= colored(text=data, color=color, on_color=on_color,attrs=None)
	if runtime['engineMode']==ENGINE_MODE.THREAD:	
		logging._acquireLock()
	sys.stdout.write(msg)
	sys.stdout.flush()
	if runtime['engineMode']==ENGINE_MODE.THREAD:
		logging._releaseLock()

# 打印信息,针对输出信息的printToStdout
def printMessage(msg,color=None,bold=False,direction=1):
	if direction==1:
			# 向左对齐
			printToStdout('\r'+msg+' '*(runtime['terminal_width']-len(msg)) +'\n\r',color=color,bold=bold)
	else:# 向右对齐
		printToStdout('\r'+' '*(runtime['terminal_width']-len(msg)) +msg+'\n\r',color=color,bold=bold)