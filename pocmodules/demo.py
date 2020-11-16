# coding:utf-8

class c2Class(object):
	'''
	 __init__用来放置一些通用的数据，例如:漏洞名称、漏洞涉及系统、漏洞CVE编号、漏洞payload、漏洞验证路径
	'''
	def __init__(self):
		self.vulname = 'demo'
		self.vulsystem= ''
		self.vulversion = ''
		self.refer= ''
		self.testisok=True

		self.vulpath=''
		self.payload=''
		self.verifypath=''
		self.flag=''

	'''
	c2Func函数解析
	c2Func函数接收目标target,进行处理
	返回状态statue、数据returnData
	> 状态statue允许4个值(定义于lib/code/static.py): 
	RETRY(重试)=-1 
	FAIL(失败)=0 
	SUCCESS(成功)=1 
	MORETRY(成功,且有目标需要重试)=10

	> 数据returnData允许3种类型: 'str' [str-list] (str|str-list,str|str-list)
	> str一般为字符串对象，也允许是可以通过str()转换为string类型的对象(类定义了__str__方法)
	> str-list则为上诉对象的列表

	demo场景1:
	检测目标A是否存在漏洞vul
	存在漏洞: status=1,returnData='%s has vul'%A
	不存在漏洞: status=0,returnData=''

	demo场景2:
	爆破目标端口
	无法访问,返回: status=0,returnData=''
	发现一个端口: status=1,returnData='80'
	发现多个端口: status=1,returnData=['80','8080','9001']

	demo场景3:
	检测域名a.com(1级域名)的2、3级域名
	target为1级域名,程序生成大量需要爆破的2级域名,并返回: status=-1,returnData=[a.a.com,b.a.com,c.a.com,%col%.a.com ...]
	target为2级域名,程序检测发现不存在该域名,返回: status=0,returnData=''
	target为2级域名,程序检测发现存在该域名,并继续生成大量需要爆破的3级域名,返回: status=10,returnData=('www.a.com',[a.www.a.com,b.www.a.com,c.www.a.com,%col%.www.a.com ...])
	target为3级域名,程序检测发现不存在该域名: status=0,returnData=''
	target为3级域名,程序检测发现存在该域名: status=1,returnData='image.www.a.com'
	

	注意：由于当前程序的运行路径和本模块文件不一致，
	      所以如果需要读取外部文件a.txt，应该使用如下方法：
	1、直接使用a.txt的绝对路径进行读取
	2、将a.txt放置在本文件目录下，获取本文件的目录`os.path.dirname(os.path.abspath(__file__))`并os.path.join拼接a.txt，进行读取
	3、将a.txt放置在data/目录下，可通过data/a.txt 进行读取
	'''
	def c2Func(self,target):
		status = 0
		returnData = ''
		return status,returnData

if __name__ == '__main__':
	target='hello'
	pocObj=c2Class()
	print(pocObj.c2Func(target))