# coding:utf-8
# 以下3行是为了协程模式。为什么这3行代码要放在代码最前面 而不是放在需要调用gevent前的地方，因为py3要求这3行代码必须在最前面，py2无这要求。
# 20210116 这3行代码放在前面运行，win10运行了，一段时间后会奔溃。。。
# import gevent
# from gevent import monkey # gevent需要修改python自带的一些标准库,以达到IO阻塞时可以切换协程运行的目的,这一过程通过monkey patch完成
# monkey.patch_all()
import time
import threading
import traceback
try:import queue as Queue # 兼容py2、3
except:import Queue
import func_timeout # 为了给c2Class文件中的函数限时所需
from lib.core.data import conf,logger,runtime,prepare
from lib.core.static import CUSTOM_LOGGING,ENGINE_MODE,RETURN_STATUS
from lib.core.common import threadLock,printToStdout,callStack
from thirdparty.terminal import get_terminal_size

# 并发引擎初始化,各种变量生成与赋值
def initCoreEngine(initFunc):
	runtime['startTime']= time.time() # 初始化引擎的时间
	logger.log(CUSTOM_LOGGING.INFO,'Start to initialize the module [%s] engine configuration ...'%prepare['nowModuleName'])
	initFunc() # 执行不同类型引擎所专用的初始化方法
	runtime['engineMode'] = conf['ENGINE'] # 引擎的类型
	runtime['concurrentNum'] = conf['CONCURRENT_NUM'] # 并发数
	runtime['c2ClassObj'] = prepare['nowc2Class']() # 当前并发类对象
	runtime['c2Func'] = getattr(runtime['c2ClassObj'],'c2Func') # 当前并发方法对象
	runtime['moduleName'] = prepare['nowModuleName'] # 并发模块名
	runtime['concurrentCount'] = runtime['concurrentNum'] # 当前可并发数量,也就是当前允许运行的scan方法的数量
	runtime['scannedCount'] = 0 # 已扫描的目标的数量
	runtime['foundCount'] = 0 # 已发现的目标的数量(c2Func方法返回1或10)	
	runtime['handleIsError'] = False # 运行scan方法中是否发生了异常
	runtime['isContinue'] = True # 并发引擎继续运行标志
	runtime['terminal_width'] = get_terminal_size()[0]-2 # 当前命令行终端的宽度 (-2:因为需要容纳控制字符\n\r)
	runtime['allTarget'] = Queue.PriorityQueue() # 需要处理的目标队列
	runtime['allTarget'].queue.extend(prepare['allTarget']) # 导入预备数据中目标列表
	runtime['debug'] = conf['DEBUG_MODE'] # 设置debug模式

	runtime['nowWait'] = [1 for i in range(runtime['concurrentNum'])] # 当下处于等待目标状态的所有scan方法的cid之和
	runtime['allWait'] = [0 for i in range(runtime['concurrentNum'])] # 全部处于等待目标状态的所有scan方法的cid之和

	logger.log(CUSTOM_LOGGING.SUCCESS,'Successfully initialized the module [%s] engine configuration'%prepare['nowModuleName'])

# 扫描函数
def scan(resultHandle,cid):
	# print(cid)
	c2Func = runtime['c2Func']
	# 循环获得目标并处理
	while runtime['nowWait'] != runtime['allWait'] or runtime['allTarget'].qsize()>0: # 并没有全部scan方法都在等待
		if runtime['isContinue'] == False:
			break
		# 获得具体攻击目标
		tgt = getTarget(cid)
		if tgt == None:
			time.sleep(1) # 此处休眠主要是用来快速退出的,当并发数较大时,每个方法都会在getTarget时设
			# 置对应的等待位,只有全部方法等待位都设置了才会使得方法退出,如果不进行休眠而是直接continue,
			# 则所有方法必须等待 并发数*runCoreEngine中while循环中的休眠时间0.01 之后,才会
			# 使得runtime['nowWait'] == runtime['allWait'],从而全部退出
			continue
		try:
			# 开始运行c2Func函数,如果c2Func函数内有异常未处理从而在这里被捕捉,则程序将会停止运行
			status,returnData = c2Func(target=tgt) # 结果状态,返回数据(一般用来存储运行结果)
			resultHandle(tgt,status,returnData) # 执行不同类型引擎所专用的结果处理方法
			if status == RETURN_STATUS.SUCCESS or status == RETURN_STATUS.MORETRY:
				modifyFoundCount() # 增加已出现数
		except func_timeout.exceptions.FunctionTimedOut as e: # 在c2Class文件中 导入模块func_timeout，并在对应函数前使用装饰器 @func_timeout.func_set_timeout(3) 可以限制对应函数运行时间为3秒
			pass
		except Exception as e:
			runtime['handleIsError'] = True
			runtime['errMsg'] = traceback.format_exc() # 获得异常回溯信息
			runtime['isContinue'] = False

		modifyScannedCount() # 增加已扫描数
		printEngineState() # 打印引擎状态
	
	# 运行到这里,说明getTarget()的结果为None,即处理目标队列为空
	modifyConcurrentCount() # 增加已扫描数
	printEngineState()

# 运行引擎,并发运行scan方法
@callStack
def runCoreEngine(resultHandle,endFunc):
	logger.log(CUSTOM_LOGGING.INFO,'Start concurrency of c2Func of the module: [%s]'%runtime['moduleName'])
	# 线程模式下
	if runtime['engineMode'] == ENGINE_MODE.THREAD:
		# 生成扫描线程集
		threads=[threading.Thread(target=scan,args=(resultHandle,i),name=str(i)) for i in range(runtime['concurrentNum'])]
		# 扫描线程集的线程中依次执行setDaemon(True)-设置主线程为子线程的守护线程、start()
		for i in  range(runtime['concurrentNum']):
			t=threading.Thread(target=scan,args=(resultHandle,i),name=str(i))
			t.setDaemon(True)
			t.start()
		# 上行代码等于以下代码（仅适用于py2，py3更新了map方法）
		# map(lambda t:t.setDaemon(True)==t.start(),threads) # ==的意义：使得该匿名函数可以依次运行t.setDaemon(True)与t.start()
		
		# 该while循环的作用：
		# 使得主线程在除了 情况1)扫描线程集内的线程全部停止(无scan运行) 或者 情况2)未全部停止,而引擎继续运行标志为假 
		# 的情况下,持续等待(time.sleep)   
		# 持续等待的原因是：
		# 保持主线程的一直存活(不会一下就运行到结束)
		# 如果用户在主线程等待期间按下ctrl+c,则主线程报出KeyboardInterrupt异常,直接跳回lib\cli.py进行退出,
		# 又由于线程集的守护线程设置为主线程(t.setDaemon(True)),则所有线程也会陆续退出
		# Q：既然是让主线程等待,为什么不使用t.join？ 
		# A：因为t.join后,当用户想通过ctrl+c主动停止程序运行时,效果很差(多线程运行下,每个线程都占用了一定时间,基本无法立刻停止)
		while 1:
			if runtime['concurrentCount'] > 0 and runtime['isContinue'] == True:
				time.sleep(0.01)
			else:
				break
	# 协程模式下
	elif runtime['engineMode'] == ENGINE_MODE.GEVENT:
		import gevent
		from gevent import monkey # gevent需要修改python自带的一些标准库,以达到IO阻塞时可以切换协程运行的目的,这一过程通过monkey patch完成
		monkey.patch_all()
		while runtime['allTarget'].qsize() > 0 and runtime['isContinue'] == True:
			gls=[] # gevent-lists 协程集
			for i in range(runtime['concurrentNum']): # 在并发数内
				if runtime['allTarget'].qsize() > 0:
					gls.append(gevent.spawn(scan,resultHandle,i)) # 执行协程
				else:
					break
			gevent.joinall(greenlets=gls) # 直到全部协程运行结束
		# 以上代码也可以使用以下代码替换
		# while runtime['allTarget'].qsize()>0 and  runtime['isContinue'] ==True:
		# 	gevent.joinall(greenlets=[gevent.spawn(scan,resultHandle,i) for i in range(runtime['concurrentNum']) if runtime['allTarget'].qsize()>0])
	printToStdout('\n')
	# 进行错误信息输出
	if 'errMsg' in runtime.keys(): # 如果runtime设置了errMsg键
		# logger.error('111111111111111111111111111111111111111111111111111111111111111111')
		logger.error(runtime['errMsg'])
	endFunc() # 执行不同类型引擎所专用的结束方法
	logger.log(CUSTOM_LOGGING.SUCCESS,'Complete concurrency of c2Func of the module: [%s]'%runtime['moduleName'])


# 获得攻击目标
@threadLock(lock=threading.Lock())
def getTarget(cid,timeout=0):
	# try:
	# 	return runtime['allTarget'].get(timeout=timeout)
	# except Queue.Empty as e:
	# 	return None
	# except Exception as e:
	# 	return None
	try:
		_t=runtime['allTarget'].get(timeout=timeout)
		# runtime['nowWait'].discard(cid)
		runtime['nowWait'][cid]=1
		return _t
	except Queue.Empty as e:
		pass
	except Exception as e:
		pass
	runtime['nowWait'][cid]=0
	# runtime['nowWait'].add(cid)
	return None

# 修改并发数
@threadLock(lock=threading.Lock())
def modifyConcurrentCount(num=-1):
	runtime['concurrentCount'] += num
	
# 修改已扫描的目标数
@threadLock(lock=threading.Lock())
def modifyScannedCount(num=1):
	runtime['scannedCount'] += num

# 修改已发现的目标数
@threadLock(lock=threading.Lock())
def modifyFoundCount(num=1):
	runtime['foundCount'] += num

# 打印引擎状态
def printEngineState():
	# 打印当前引擎的 已发现目标数、剩余目标数、已扫描目标数、耗时
	eMsg = '%s found | %s remaining | %s scanned | %.2f/s rate in %.2f seconds' % (
		runtime['foundCount'],runtime['allTarget'].qsize(),runtime['scannedCount'],runtime['scannedCount']/(time.time()-runtime['startTime']),
		time.time()-runtime['startTime'])
	out ='\r'+' '*(runtime['terminal_width']-len(eMsg))+eMsg
	printToStdout(out)
	# printToStdout('\r') # 经过调试发现，输出\r 使得debug模式下，可以更加整齐的显示信息.PS:20200825 测试发现,加不加没什么影响