# coding:utf-8
import threading
from lib.core.data import logger,runtime,prepare
from lib.controller.coreengine import initCoreEngine,runCoreEngine
from lib.core.static import MODULE_TYPE,RETURN_STATUS
from lib.core.setting import CLASSNAME,FUNCNAME
from lib.core.common import threadLock,printMessage


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

# 对成功的数据 进行处理
@threadLock(lock=threading.Lock())
def successHandle(tgt,successInfo):
	try:
		if isinstance(successInfo, str):
			runtime['allResult'].add(successInfo) # 加操作
		elif isinstance(successInfo, list):
			successInfo=list(map(str,successInfo)) # map函数的返回结果在py2下是list,而在py3下是map，所以这里直接再套个list
			runtime['allResult'].update(set(successInfo)) # 并操作
		else:
			successInfo=str(successInfo)
			runtime['allResult'].add(successInfo) 
	except Exception as e:
		logger.debug('The target [%s] detection result was successful, but an exception occurred when more information about the target was converted to string type.'%tgt)
		return 0
	if runtime['showMode']:
		infoMsg = "%-20s %s"%('['+str(tgt)+']',successInfo)
		printMessage(infoMsg)

# 专用的结果处理方法
def resultHandle(tgt,status,returnData):
	if status == RETURN_STATUS.RETRY:
		retryHandle(returnData)
	elif status == RETURN_STATUS.SUCCESS:
		successHandle(tgt,returnData)
	elif status == RETURN_STATUS.MORETRY:
		_success,_retry = returnData
		retryHandle(_retry)
		successHandle(tgt,_success)
	elif status == RETURN_STATUS.FAIL:
		failHandle(returnData)

# 专用的结束方法
def endFunc():
	# 将引擎的结果集导入到汇总集中
	summary.update(runtime['allResult'])

# 专用的初始化方法
def initFunc():
	runtime['allResult'] = set() # 定义 结果集合
	runtime['showMode'] = True # 是否显示成功结果

# 预处理模块的并发引擎
def Engine():
	global summary # 用于汇总所有预处理模块的运行结果
	summary =set()

	# 遍历预处理模块
	for mData in prepare[MODULE_TYPE.PRE]:
		prepare['nowc2Class'] = mData['class'] # 当前执行的处理模块的类对象
		prepare['nowModuleName'] = mData['name'] # 当前执行的处理模块名

		logger.info('The current concurrent module of the engine: [%s]'%prepare['nowModuleName'])

		initCoreEngine(initFunc)
		runCoreEngine(resultHandle,endFunc)
	# 所有的预处理模块都运行并发处理完毕了,将汇总的数据导入处理模块将要使用的预备目标集中
	l=len(summary)
	logger.info('Find target : [%d]'%l)
	prepare['allTarget'] = summary
