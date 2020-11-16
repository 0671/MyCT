# coding:utf-8
import socket
import threading
import Queue

class c2Class(object):
	def __init__(self):
		self.isRelease=True
		self.ports_spec=[21,22,23,53,69,80,81,82,83,84,85,86,87,88,89,135,139,143,443,445,465,993,995,1080,1158,1433,1521,1863,2100,3128,3306,3389,7001,8009,8009,8080,8081,8082,8083,8084,8085,8086,8087,8088,8888,9080,9090,33389,33899]
		self.ports_all=[i for i in xrange(1,65536)]
	
	def c2Func(self,target):
		status=1
		returnData=[]

		tds=[]
		rq=Queue.Queue()
		# for p in self.ports_all:
		for p in self.ports_spec:
			t=threading.Thread(target=self.check,args=(target,p,rq))
			t.setDaemon(True)
			t.start()
			tds.append(t)
		for t in tds:
			t.join()

		if rq.qsize()==0:
			status=0
		else:
			returnData.append(target+'-'+','.join(list(rq.queue)))
		return status,returnData

	# 检查目标端口
	def check(self,ip,port,rq):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.settimeout(2)
		r=sock.connect_ex((ip,port))
		sock.close()
		if r==0:
			rq.put(str(port))

if __name__ == '__main__':
	target="127.0.0.1"
	pocObj=c2Class()
	print(pocObj.c2Func(target))