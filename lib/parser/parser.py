#coding:utf-8
import argparse
import sys
import time
from lib.core.setting import VERSION
from lib.core.data import logger
from lib.parser.hander import concuNum,fileNameOfPocM,fileNameOfPreM,fileNameOfTgt,testFofa,myActionDebug
from lib.core.static import CUSTOM_LOGGING
from lib.core.setting import CONCURRENT_NUM
# 兼容python3
if sys.version[0]=='3':
	from functools import reduce

usage='''python MyCT.py [-eT|-eG] [-pm] [-m] [-iS|iF|-iN|-iR|-qF] [-o] [msic]

Example:
python MyCT.py -m demo -iS 1.1.1.1 -o
python MyCT.py -pm getWeb -m getTitleByUrl -iR 192.168.1.1-192.168.1.253
python MyCT.py -eT -m getTitleByUrl -iF urls.txt -c 50 -o titles.txt
python MyCT.py -eG -pm ljjsdb -m coremail\\CMXT5-2019-0002 -iS baidu.com -c 1000
'''


def parseArgs():
	ctParser=argparse.ArgumentParser(
		prog="MyCT", # 程序名
		description="powered by 0671 <mail: h.vi@qq.com >",# 位于输出的usage下方
		usage=usage,# 程序用法，直接输出
		add_help=False # 关闭argparse库所生成的默认帮助
		)

	# 并发引擎参数组
	ENGINE=ctParser.add_argument_group('ENGINE')
	ENGINE.add_argument('-eT',default=False,action='store_true', # 选项变量性质
		dest='engine_thread',  # 选项描述
		help='Multi-threaded engine (selected by default)') # 选项帮助
	ENGINE.add_argument('-eG',default=False,action='store_true',
		dest='engine_gevent',
		help='Gevent engine (single thread with asynchronous)')
	ENGINE.add_argument('-c',default=CONCURRENT_NUM,type=concuNum,
		dest='concurrent_number',
		help='The concurrent number of threads/gevent, 50 by default'
		)

	# 并发模块参数组
	MODULE=ctParser.add_argument_group('MODULE')
	MODULE.add_argument('-m',type=fileNameOfPocM,nargs='+',
		dest='pocmodule_path',metavar='NAME',
		help='Load concurrent modules by name (-m demo or -m xxx/xxx/xxx.py) in ./pocmodules/ '
		)
	MODULE.add_argument('-pm',type=fileNameOfPreM,
		dest='premodule_path',metavar='NAME',nargs='*',
		help='Load pre-treat concurrent modules by name (-pm demo or -pm xxx/xxx/xxx.py) in ./premodules/ ')

	# 并发目标参数组
	TARGET=ctParser.add_argument_group('TARGET')
	TARGET.add_argument('-iS',type=str,
		dest='target_single',metavar='TARGET',
		help='Scan a single target (e.g baidu.com)'
		)
	TARGET.add_argument('-iF',type=fileNameOfTgt,
		dest='target_file',metavar='FILE',
		help='Load the target from the file (e.g urls.txt)'
		)
	TARGET.add_argument('-iN',type=str,
		dest='target_network',metavar='IP/MASK',
		help='Generate target IP from IP/MASK (e.g 127.0.0.1/24)'
		)
	TARGET.add_argument('-iR',type=str,
		dest='target_iprange',metavar='IP-IP',
		help='Load the target from the ip range (e.g 10.1.1.1-10.1.1.125)'
		)
	TARGET.add_argument('-qF',type=testFofa,nargs='?',const='',
		dest='target_fofa',metavar='QUERY',
		help='Query data from Fofa API (e.g thinkphp).'\
		' If the query string contains the cmd special characters (eg. && ||), '\
		'you should just use -qf (not query string). '\
		'Later, MyCT will prompt you to enter the query string.'
		)

	# 输出结果参数组
	OUTPUT=ctParser.add_argument_group('OUTPUT')
	OUTPUT.add_argument('-o',nargs='?',type=str,
		default=None,const= time.strftime('default_[%Y%m%d-%H%M%S]', time.localtime(time.time()))+'_[%s].txt',
		dest='output_file',
		help='Output file, default by ./output/default_[time]_[module].txt'
		)

	# 其他选项 参数组
	MSIC=ctParser.add_argument_group('MSIC')
	MSIC.add_argument('--single',default=False,action='store_true',
		dest='single_mode',
		help="Exit after the module's c2Func method return True"
		)
	MSIC.add_argument('--debug',default=False,action=myActionDebug,
		dest='debug_mode',
		help='Show more debugging information'
		)
	MSIC.add_argument('--show',default=False,action='store_true',
		dest='show_modules',
		help='Show the available module names under ./modules/, then exit'
		)
	MSIC.add_argument('-v','--version',action='version',version=VERSION,
		help="Show the version of the program and exit"
		)
	MSIC.add_argument('-h','--help',action='help',
		help='Show help message and exit'
		)

	# 如果命令行参数只有MyCT.py,则添加-h参数
	if len(sys.argv)==1:
		sys.argv.append('-h')
	sys_argv=reduce(lambda x,y:x+' '+y,sys.argv)
	logger.log(CUSTOM_LOGGING.SUCCESS,'User typed: %s'%sys_argv)
	# 解析命令行参数
	args=ctParser.parse_args()
	logger.log(CUSTOM_LOGGING.SUCCESS,'The parameters are parse successfully.\nParameters are as follows: \n[%s]'%args)
	return args
