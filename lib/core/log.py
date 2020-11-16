#coding:utf-8
import logging
import sys
from lib.core.static import CUSTOM_LOGGING
from thirdparty.ansistrm import ColorizingStreamHandler

# 自定义日志类型
logging.addLevelName(CUSTOM_LOGGING.ERROR,'ERROR')
logging.addLevelName(CUSTOM_LOGGING.WARNING,'WARNING')
logging.addLevelName(CUSTOM_LOGGING.SUCCESS,'SUCCESS')
logging.addLevelName(CUSTOM_LOGGING.INFO,'INFO')

# 设置根记录器的记录日志级别
# 根记录器设置为CUSTOM_LOGGING.INFO，就是1，最小的日志级别,也就是所有日志都会输出
logging.getLogger().setLevel(CUSTOM_LOGGING.INFO)

# 获得ctLog记录器
LOGGER=logging.getLogger('ctLog')

# 获得日志输出器 
# 文件输出器：file_hd
# 命令行输出器：cmd_hd，这里使用了一个彩色输出类的对象
file_hd=logging.FileHandler(filename='myct.log',mode='w',encoding='utf-8')
cmd_hd=ColorizingStreamHandler()

# 设置命令行输出器cmd_hd的输出日志级别
# cmd_hd设置为logging.INFO，就是20，则所有级别>=20 的日志就会输出
cmd_hd.setLevel(logging.INFO)

#  修改输出器cmd_hd内部的日志彩色序列，cmd_hd是依据该序列进行彩色输出
cmd_hd.level_map[logging.getLevelName("INFO")] = (None, "cyan", False)
cmd_hd.level_map[logging.getLevelName("SUCCESS")] = (None, "green", False)
cmd_hd.level_map[logging.getLevelName("WARNING")] = (None, "yellow", False)
cmd_hd.level_map[logging.getLevelName("ERROR")] = (None, "red", False)

# 获取格式化程序：common_fmt、debug_fmt，
common_fmt=logging.Formatter(fmt="[%(asctime)s] [%(levelname)s] %(message)s",datefmt="%H:%M:%S")
debug_fmt=logging.Formatter(fmt="[%(asctime)s] [%(levelname)s] [%(filename)s] %(message)s",datefmt="%Y-%m-%d %H:%M:%S")

# 给输出器 设置 格式化程序
cmd_hd.setFormatter(common_fmt)
file_hd.setFormatter(debug_fmt)

# 给记录器 设置 输出器
LOGGER.addHandler(cmd_hd)
LOGGER.addHandler(file_hd)

def DEBUG(): # 开启调试模式
	# 重新设置输出的日志级别和日志格式
	LOGGER.removeHandler(cmd_hd)
	cmd_hd.setLevel(CUSTOM_LOGGING.INFO)
	cmd_hd.setFormatter(debug_fmt)
	LOGGER.addHandler(cmd_hd)