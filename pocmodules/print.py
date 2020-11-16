# coding:utf-8
import os

class c2Class(object):
	def __init__(self):
		pass
	def c2Func(self,target):
		status=1
		returnData='%s'%str(target)
		return status,returnData

if __name__ == '__main__':
	target='hello'
	pocObj=c2Class()
	print(pocObj.c2Func(target))