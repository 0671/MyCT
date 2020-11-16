# coding:utf-8
from lib.core.log import LOGGER

# https://blog.csdn.net/codingwithme/article/details/41675679
# 日志记录器
logger=LOGGER

# 命令行参数
args=None

paths={}
# 程序路径
# ROOT_PATH  程序根路径
# POCMODULE_PATH  处理模块路径
# PREMODULE_PATH  预处理模块路径
# OUTPUT_PATH  默认输出路径
# DATA_PATH  数据路径
# 定义于lib\core\common.py的setPaths方法中

conf={}
# 程序配置
# ENGINE  引擎类型
# CONCURRENT_NUM  并发数
# POCMODULE_NUM  处理模块数
# POCMODULES  处理模块信息列表
# PRE_TREAT  是否需要预处理
# PREMODULE_NUM  预处理模块数
# PREMODULES  预处理模块信息列表
# TARGET_TYPE  并发目标类型
# TARGET  并发目标集合
# OUTPUT_MODE  输出模式
# OUTPUT_FILE  输出文件名
# OUTPUT_FILE_PATH  结果输出文件完整路径
# DEBUG_MODE  调试模式
# SINGLE_MODE  简单模式

# PS:
# POCMODULES、PREMODULES 结构:[{'fullPath':...,'name':...}] fullPath:模块完整路径 name:模块名
# 定义于lib\core\config.py的moduleRegister方法中

prepare={}
# 引擎运行的预备数据
# Poc、Pre 结构:[{'class':...,'name':...}] class:并发类对象 name:模块名
# allTarget 列表 并发目标
# nowc2Class 当前执行的处理模块的类对象,其实就是prepare['Poc']、prepare['Pre']列表中的元素的class
# nowModuleName 当前执行的处理模块名,其实就是prepare['Poc']、prepare['Pre']列表中的元素的name


runtime={}
# 并发引擎运行时的数据
# startTime 引擎运行时间
# engineMode 引擎类型
# concurrentNum 并发数
# c2ClassObj 当前并发类对象
# c2Func 当前并发方法对象
# moduleName 并发模块名
# concurrentCount 当前可并发数量
# scannedCount 已扫描的目标的数量
# foundCount 已发现的目标的数量
# handleIsError 运行scan方法中是否发生了异常
# isContinue 是否继续运行并发引擎
# terminal_width 当前命令行终端的宽度
# allTarget 需要处理的目标队列
# debug debug模式