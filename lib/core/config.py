# coding:utf-8
import os
import sys
import time
from lib.core.common import ValueInfoInList
from lib.core.data import paths,conf,logger
from lib.core.log import DEBUG,LOGGER
from lib.core.static import ENGINE_MODE,CUSTOM_LOGGING,TARGET_TYPE,OUTPUT_MODE


# 初始化程序配置
def initConfig(args):
	checkShow(args) # 展示模块
	engineRegister(args) # 并发引擎注册
	moduleRegister(args) # 并发模块注册
	targetRegister(args) # 输入目标注册
	outputRegister(args) # 输出对象注册
	misc(args) # 杂项
	logger.log(CUSTOM_LOGGING.SUCCESS,'Initial configuration completed')

def checkShow(args):
	if args.show_modules:
		pocmodulePaths=[] # 处理模块路径集
		premodulePaths=[] # 预处理模块路径集
		# os.walk() 方法用于通过在目录树中游走，输出在目录中的根路径、文件夹的相对路径、文件的相对路径
		for root,dirs,files in os.walk(paths['POCMODULE_PATH']):
			for name in files:
				_modulepath=os.path.join(root, name)
				if _modulepath.lower().endswith('py'):
					pocmodulePaths.append(_modulepath)
		for root,dirs,files in os.walk(paths['PREMODULE_PATH']):
			for name in files:
				_modulepath=os.path.join(root, name)
				if _modulepath.lower().endswith('py'):
					premodulePaths.append(_modulepath)		
		pocmoduleNum=len(pocmodulePaths)
		premoduleNum=len(premodulePaths)
		pocMsg=''
		preMsg=''
		for _str in pocmodulePaths:
			_str=_str.split(paths['POCMODULE_PATH'])[1][1:]
			moduleName=os.path.splitext(_str)[0]
			if moduleName == '__init__': # 初始化脚本，不计入模块中
				pocmoduleNum-=1
			else:
				pocMsg+=' %s\n'%moduleName
		for _str in premodulePaths:
			_str=_str.split(paths['PREMODULE_PATH'])[1][1:]
			moduleName=os.path.splitext(_str)[0]
			if moduleName == '__init__':
				premoduleNum-=1
			else:
				preMsg+=' %s\n'%moduleName
		pocMsg='Poc Module Name (total:%s)\n' % str(pocmoduleNum)+pocMsg
		preMsg='Pre Module Name (total:%s)\n' % str(premoduleNum)+preMsg
		logger.info(preMsg)
		logger.info(pocMsg)
		sys.exit(0)

def engineRegister(args):
	checkList= [args.engine_gevent,args.engine_thread]
	seted,index = ValueInfoInList(checkList,True)
	if seted <= 1: # seted=1说明设置eT或eG  seted=0说明未设置,则默认eT
		conf['ENGINE'] = ENGINE_MODE.GEVENT if index == 0 else ENGINE_MODE.THREAD
		conf['CONCURRENT_NUM'] = args.concurrent_number
	else:
		msg='Too many options in [-eT|-eG]'
		sys.exit(logger.error(msg))

def moduleRegister(args):
	# 在parser\handler.py中已经对module文件的真实存在性进行了检验
	# 所以现在只需要对conf中的POCMODULE_NUM、POCMODULES、PREMODULE_NUM、PREMODULES进行赋值
	if args.pocmodule_path != None:
		conf['POCMODULE_NUM'] = len(args.pocmodule_path)
		conf['POCMODULES'] = []
		for _modulePath in args.pocmodule_path:
			mInfo={}
			mInfo['fullPath'] = _modulePath # 模块路径
			mInfo['name'] = _modulePath[len(paths['POCMODULE_PATH'])+1:-3] #  模块名,更为清晰
			# mInfo['name'] = os.path.split(_modulePath)[1][:-3] # 模块名
			conf['POCMODULES'].append(mInfo)
	else:
		msg='Too few options in [-m]'
		sys.exit(logger.error(msg))
	if args.premodule_path != None:
		conf['PRE_TREAT'] = True
		conf['PREMODULE_NUM'] = len(args.premodule_path)
		conf['PREMODULES']=[]
		for _modulePath in args.premodule_path:
			mInfo={}
			mInfo['fullPath'] = _modulePath # 模块路径
			mInfo['name'] = _modulePath[len(paths['PREMODULE_PATH']):-3].replace('\\','/') #  模块名,更为清晰
			mInfo['name'] = os.path.split(_modulePath)[1][:-3] # 模块名
			conf['PREMODULES'].append(mInfo)
	else:
		conf['PRE_TREAT'] = False

def targetRegister(args):
	def _single():
		conf['TARGET_TYPE'] = TARGET_TYPE.SINGLE
		conf['TARGET'] = args.target_single
	def _file():
		conf['TARGET_TYPE'] = TARGET_TYPE.FILE
		conf['TARGET']=args.target_file
	def _network():
		conf['TARGET_TYPE'] = TARGET_TYPE.NETWORK
		conf['TARGET'] = args.target_network
	def _iprange():
		conf['TARGET_TYPE'] = TARGET_TYPE.IPRANGE
		conf['TARGET'] = args.target_iprange
	def _fofa():
		conf['TARGET_TYPE'] = TARGET_TYPE.FOFA
		conf['TARGET'] = args.target_fofa
	_fun=[_single,_file,_network,_iprange,_fofa] # 函数列表
	checkList=[args.target_single,args.target_file,args.target_network,args.target_iprange,args.target_fofa]
	# _fun中的元素顺序与checkList的元素顺序都是相关联的，一一对应的
	seted,index=ValueInfoInList(checkList,None,3)
	if seted == 1: # 设置了一个值
		_fun[index]()
	elif seted > 1: # 设置了多个值
		msg='Too more options in [-iS|iF|-iN|-iR|-qF]'
		sys.exit(logger.error(msg))
	else: # 未设置值
		msg='Too few options in [-iS|iF|-iN|-iR|-qF]. Please use [-iS|iF|-iN|-iR|-qF] to set your target'
		sys.exit(logger.error(msg))

def outputRegister(args):
	if args.output_file != None: # 如果输出文件名不为None，说明用户已经设置了-o参数
		conf['OUTPUT_MODE'] = OUTPUT_MODE.ALL # 全输出(即输出屏幕，又输出文件)
		conf['OUTPUT_FILE'] = args.output_file
		if conf['OUTPUT_FILE'].startswith('default_['): # 如果是MyCT默认生成的输出文件，需要填入模块名
			conf['OUTPUT_FILE_PATH'] = os.path.join(
				paths['OUTPUT_PATH'],conf['OUTPUT_FILE']%(conf['TARGET'].replace('/','')))
		else:
			conf['OUTPUT_FILE_PATH'] = os.path.join(
				paths['OUTPUT_PATH'],conf['OUTPUT_FILE'])

		open(conf['OUTPUT_FILE_PATH'],mode='w').close()
	else:
		conf['OUTPUT_MODE']=OUTPUT_MODE.SCREEN

def misc(args):
	conf['DEBUG_MODE']=args.debug_mode
	conf['SINGLE_MODE']=args.single_mode

# args的变量如下：
# engine_thread 线程引擎标志
# engine_gevent 协程引擎标志
# concurrent_number 并发数
# pocmodule_name 处理模块的路径列表
# premodule_name 预处理模块的路径列表
# target_single 简单目标
# target_file 目标文件
# target_network 目标网络
# target_iprange 目标ip区间
# output_file 输出文件名
# output_file_status 禁止输出文件标志
# single_mode 简单模式
# debug_mode 调试模式
# show_modules 展示攻击模块标识

# conf中的键如下：
# ENGINE：引擎类型
# CONCURRENT_NUM：并发数
# POCMODULE_NUM：处理模块数
# POCMODULES：处理模块信息列表
# PRE_TREAT：是否需要预处理
# PREMODULE_NUM：预处理模块数
# PREMODULES：预处理模块信息列表
# TARGET_TYPE：并发目标类型
# TARGET：并发目标集合
# OUTPUT_MODE：输出模式
# OUTPUT_FILE：输出文件名
# OUTPUT_FILE_PATH：结果输出文件路径
# DEBUG_MODE：调试模式
# SINGLE_MODE：简单模式