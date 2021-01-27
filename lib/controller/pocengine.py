# coding:utf-8
import threading
import codecs
from lib.core.data import conf,logger,runtime,prepare
from lib.controller.coreengine import initCoreEngine,runCoreEngine
from lib.core.static import OUTPUT_MODE,MODULE_TYPE,RETURN_STATUS
from lib.core.setting import CLASSNAME,FUNCNAME
from lib.core.common import threadLock,printMessage
# 兼容python3
import sys
if sys.version[0]=='3':
	from functools import reduce

# 对需要重新加入目标队列的数据 进行处理
@threadLock(lock=threading.Lock())
def retryHandle(retryInfo):
	if isinstance(retryInfo, str):
		runtime['allTarget'].put(retryInfo)
	elif isinstance(retryInfo, list):
		runtime['allTarget'].queue.extend(retryInfo)
	else:
		runtime['allTarget'].put(retryInfo)

# 对失败数据 进行处理
def failHandle(failInfo):
	pass

# 对需要成功的数据 进行处理
@threadLock(lock=threading.Lock())
def successHandle(tgt,successInfo):
	runtime['allSuccess']+=1
	try:
		if isinstance(successInfo, str):
			pass
		elif isinstance(successInfo, list): # 列表则拼接为字符串
			successInfo = reduce(lambda x,y:str(x)+','+str(y),successInfo)
		else:
			uccessInfo=str(successInfo)
	except Exception as e:
		successInfo='The target [%s] detection result was successful, but an exception occurred when outputting more information.'%str(tgt)
		logger.debug(successInfo)
	stdMsg = "[!] %s"%successInfo
	printMessage(stdMsg,'red',True) # 输出成功数据到命令行
	if runtime['outputMode'] == OUTPUT_MODE.ALL:
		fileMsg = "%-20s %s"%('['+str(tgt)+']',successInfo)
		write2File(fileMsg) # 输出成功数据到文件
	if runtime['singleMode']: # 如果是单结果模式
		runtime['isContinue'] = False # 设置停止运行标识
		printMessage('[single-mode] found!','red',True) # 打印提示

# 专用的结果处理方法
def resultHandle(tgt,status,returnData):
	if status == RETURN_STATUS.RETRY:
		retryHandle(returnData)
	elif status == RETURN_STATUS.SUCCESS:
		successHandle(tgt,returnData)
	elif status == RETURN_STATUS.MORETRY:
		_success,_retry = returnData
		successHandle(tgt,_success)
		retryHandle(_retry)
	elif status == RETURN_STATUS.FAIL:
		failHandle(returnData)

# 写入到文件
@threadLock(lock=threading.Lock())
def write2File(msg):
	try:
		with codecs.open(runtime['outputFilePath'],'a','utf-8') as f:
			f.write(msg+'\n')	
	except UnicodeDecodeError as e: # 如果出现unicode解码异常，则使用py默认读写
		with open(runtime['outputFilePath'],'a') as f:
			f.write(msg+'\n')

# 专用的结束方法
def endFunc():
	pass

def initFunc():
	runtime['allSuccess'] =0 # 测试成功数
	runtime['singleMode'] = conf['SINGLE_MODE'] # 单结果模式
	runtime['outputMode'] = conf['OUTPUT_MODE'] # 输出方式
	if runtime['outputMode'] == OUTPUT_MODE.ALL:
		runtime['outputFilePath'] = conf['OUTPUT_FILE_PATH'] # 输出文件路径

def Engine():
	# 遍历预处理模块
	for mData in prepare[MODULE_TYPE.POC]:
		prepare['nowc2Class'] = mData['class'] # 当前执行的处理模块的类对象
		prepare['nowModuleName'] = mData['name'] # 当前执行的处理模块名

		logger.info('The current concurrent module of the engine: [%s]'%prepare['nowModuleName'])

		initCoreEngine(initFunc)
		runCoreEngine(resultHandle,endFunc)

		logger.info('Find [%s] Vuls : [%d]'%(prepare['nowModuleName'],runtime['allSuccess']))