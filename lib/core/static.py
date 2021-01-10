#coding:utf-8

# 自定义日志类型
class CUSTOM_LOGGING:
	INFO = 3
	SUCCESS = 5
	WARNING = 7
	ERROR = 9

# 模块类型
class MODULE_TYPE:
	PRE = 'Pre'
	POC = 'Poc'

# 并发引擎模式
class ENGINE_MODE:
	THREAD = 9
	GEVENT = 8

# 攻击目标类型
class TARGET_TYPE:
	SINGLE = 0
	FILE = 1
	NETWORK = 2
	IPRANGE = 3
	FOFA = 4
	SHODAN = 5
	ZOOMEYE = 6

# 并发函数返回状态
class RETURN_STATUS:
	RETRY = -1
	FAIL = 0
	SUCCESS = 1
	MORETRY = 10

# 结果输出方式
class OUTPUT_MODE:
	ALL = 9
	FILE = 8
	SCREEN = 7
