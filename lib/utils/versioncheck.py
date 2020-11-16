# coding:utf-8

import sys

PYVERSION = sys.version.split()[0]
# sys.version 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17) [MSC v.1500 64 bit (AMD64)]

# 检查py版本，运行MyCT的py版本需要位于[2.6,3)之间
if PYVERSION >= "3" or PYVERSION < "2.6":
	exit("[CRITICAL] incompatible Python version detected ('%s'). "
		"For successfully running this project, you'll have to use version 2.6 or 2.7 "
		"(visit 'http://www.python.org/download/')" %PYVERSION)

# 检查当前py是否拥有了以下的核心拓展库
extensions = ("gzip","ssl","sqlite3","zlib")
try:
	for e in extensions:
		__import__(e)
except ImportError:
	errMsg = "missing one or more core extensions (%s) "%(",".join("'%s'"%e for e in extensions))
	errMsg += "most probably because current version of Python has been "
	errMsg += "built without appropriate dev packages (e.g. 'libsqlite3-dev')"
	exit(errMsg)
