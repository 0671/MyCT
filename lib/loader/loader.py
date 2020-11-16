# coding:utf-8
import imp
import sys
import re
import os
from thirdparty import IPy
from lib.core.common import intRange
from lib.core.data import prepare,conf,logger
from lib.core.setting import CLASSNAME,FUNCNAME
from lib.core.static import CUSTOM_LOGGING,TARGET_TYPE,MODULE_TYPE


# 载入攻击目标
def loadTarget():
	infoMsg = 'Start loading targets'
	logger.log(CUSTOM_LOGGING.INFO,infoMsg)

	prepare['allTarget'] = set() # 目标使用列表存放

	# 以下为不同目标类型对应的处理方法
	def _single(): # 简单目标
		prepare['allTarget'].add(str(conf['TARGET']))
	def _file(): # 目标为文件
		for line in open(conf['TARGET'],'r'):
			tgt = line.strip()
			if tgt:
				prepare['allTarget'].add(tgt)
	def _network(): # 目标为网段,需要符合Ipy.IP()的形参要求
		try:
			ips = IPy.IP(conf['TARGET'])
			for i in ips:
				prepare['allTarget'].add(i.strNormal())
		except Exception as e:
			errMsg = "Invalid IP/MASK : %s"%e
			sys.exit(logger.error(errMsg))
	def _iprange(): # 目标为IP地址范围
		rcIp = re.compile(r'((?:\d{1,3}\.){3}\d{1,3})-((?:\d{1,3}\.){3}\d{1,3})')
		_ip = rcIp.findall(str(conf['TARGET']))[0] # 正则提取IP-IP格式下的IP地址
		try:
			if len(_ip) == 2: # 提取到2个IP地址
				ipStart,ipEnd = [IPy.IP(i).int() for i in _ip] # 将首尾IP地址转换为ip对应的数值
				ipsInt = intRange(ipStart,ipEnd) # 获得首尾范围下数值生成器
			else:
				raise ValueError
			for i in ipsInt:
				prepare['allTarget'].add(IPy.IP(i).strNormal())
		except ValueError as e:
			errMsg = "Invalid IP-Range : %s .The correct IP-Range is such as : 192.168.1.1-192.168.2.1"%conf['TARGET']
			sys.exit(logger.error(errMsg))

	# _func是一个方法列表，方法的下标和lib\core\static.py的TARGET_TYPE内的元素值一一对应
	_func = [_single,_file,_network,_iprange]
	_func[conf['TARGET_TYPE']]() # 调用对应目标类型的处理目标方法

	msg = 'Successfully loaded all targets'
	logger.log(CUSTOM_LOGGING.SUCCESS,msg)

# 载入模块的底层方法
def _loadModule(mType,mList,mNum): # mType:模块类型 mList:模块信息列表 mNum:模块数
	prepare[mType] = []
	for mInfo in mList:
		mData = {} # 存储模块对象
		mName = mInfo['name'] # 模块名称
		mFullPath = mInfo['fullPath'] # 模块文件完整路径
		infoMsg = 'Start to load the module : %s'%mName
		logger.log(CUSTOM_LOGGING.INFO,infoMsg)
		# 寻找模块
		filehandle,pathname,description = imp.find_module(mName,[os.path.dirname(mFullPath),])
		try:
			# 导入模块
			mObj = imp.load_module(mName,filehandle,pathname,description)
			# 检查模块中必须存在的类CLASSNAME与方法FUNCNAME
			if not hasattr(mObj,CLASSNAME):
				errMsg = "Can't be found the concurrency class : '%s' in current module [%s]"%(CLASSNAME,mName)
				sys.exit(logger.error(errMsg))
			if not hasattr(getattr(mObj,CLASSNAME,None),FUNCNAME):
				errMsg = "Can't be found the concurrency function: '%s' in current module [%s]"%(FUNCNAME,mName)
				sys.exit(logger.error(errMsg))

			mData['class'] = getattr(mObj,CLASSNAME,None) # 并发类
			mData['name'] = mName # 模块名
			prepare[mType].append(mData) # 将并发类与模块名赋值给prepare变量中
		except ImportError as e: # 如果在导入模块中发生ImportError,说明有可能模块中import了pip未安装的py库
			errMsg = "An exception occurred when loading [%s.py].\nException : %s\nYou can use pip to download the module."%(mName,str(e))
			sys.exit(logger.error(errMsg))
		msg = 'Successfully loaded the module : %s'%mName
		logger.log(CUSTOM_LOGGING.SUCCESS,msg)

# 载入处理模块
def loadPocModule():
	_loadModule(MODULE_TYPE.POC,conf['POCMODULES'],conf['POCMODULE_NUM'])

# 载入预处理模块
def loadPreModule():
	_loadModule(MODULE_TYPE.PRE,conf['PREMODULES'],conf['PREMODULE_NUM'])

# 载入模块
def loadModule():
	loadPocModule()
	if conf['PRE_TREAT']:
		loadPreModule()
	msg = 'Successfully loaded all modules'
	logger.log(CUSTOM_LOGGING.SUCCESS,msg)