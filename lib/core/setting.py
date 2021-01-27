# coding:utf-8
import subprocess,os

VERSION = "1.0"
PROJECT = "MyCT"
AUTHOR= "0671"
MAIL = 'h.vi@qq.com'
PLATFORM = os.name
LICENS = 'GPLv2'

try:
	IS_WIN = subprocess.mswindows
except:
	IS_WIN = subprocess._mswindows
ISCALLGRAPH = True # 是否生成程序的函数调用图.注意：在协程模式下不支持！

# 并发模块类名 与 类中的并发函数
CLASSNAME = 'c2Class'
FUNCNAME = 'c2Func'

# 默认并发数
CONCURRENT_NUM = 50

# 相对路径
RELATIVE_PATH = {
'POCMODULE':'pocmodules',
'PREMODULE':'premodules',
'OUTPUT':'output',
'DATA':'data'}

# 使用API所需要的数据
API_KEY= {
	'Fofa':{
	'email':'xxxxxxxx',
	'key':'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'size':100 # 【普通会员】免费前100条/次 【高级会员】免费前10000条/次 【企业会员】免费前100,000条/次 check in https://fofa.so/static_pages/vip
	}
}

# 图标
BANNER ='''
\033[04;31m    __  ___      ____________  \033[0m
\033[04;32m   /  |/  /_  __/ ____/_  __/  \033[0m
\033[04;33m  / /|_/ / / / / /     / /     \033[0m
\033[04;34m / /  / / /_/ / /___  / /      \033[0m
\033[04;35m/_/  /_/\__, /\____/ /_/       \033[0m
\033[04;36m       /____/ \033[0m Version:%s mail:%s\n'''%(VERSION,MAIL)
# print(u"(^-^*)")