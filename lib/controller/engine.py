# coding:utf-8
from lib.core.data import conf,runtime
from lib.controller.pocengine import Engine as pocEngine
from lib.controller.preengine import Engine as preEngine

# 启动并发引擎
def run():
	if conf['PRE_TREAT']:
		preEngine() # 启动针对预处理模块的并发引擎
	runtime=[] # 重置运行时的数据
	pocEngine() # 启动针对处理模块的并发引擎