import asyncio
import re
import ssl

import websockets
import json



async def main_logic(t):
    rc_user_id=re.compile(r'(?<=user_id=)[a-z-0-9\-]{36}')
    rc_asset_id=re.compile(r'(?<=asset_id=)[a-z-0-9\-]{36}')
    rc_system_user_id=re.compile(r'(?<=system_user_id=)[a-z-0-9\-]{36}')

    text=''
    count=0
    # print("#######start ws")
    async with websockets.connect(t) as client:
        await client.send(json.dumps({"task": "//opt/jumpserver/logs/jumpserver"}))
        while 1:
            ret = json.loads(await client.recv())['message']
            # print(ret,end='')
            count+=1
            print('[*] Get log %d'%count)
            fu=rc_user_id.findall(ret)
            fa=rc_asset_id.findall(ret)
            fs=rc_system_user_id.findall(ret)
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
                print('[!] Now monitoring found: %s'%text)
        # print('[!]%s can read log'%t)


async def read_gunicorn(t):
    # print("#######start ws")
    clean_pattern = re.compile(r"^.+?/(?:v1/terminal/terminals/|health/).+?$", re.M | re.I)
    async with websockets.connect(t) as client:
        await client.send(json.dumps({"task": "//opt/jumpserver/logs/gunicorn"}))
        while True:
            ret = json.loads(await client.recv())
            print(clean_pattern.sub(ret["message"], ""), end="")


if __name__ == "__main__":
    url = "/ws/ops/tasks/log/"
    try:
        i='https://jump.rntd.cn/'
        host = i.strip('/')
        # host = 'http://61.153.40.102:8888'
        # print("##################")
        target = host.replace("https://", "wss://").replace("http://", "ws://")+url
        target='ws://211.157.143.22:8082/ws/ops/tasks/log/'
        print(target)
        # print("target: %s" % (target,))
        asyncio.get_event_loop().run_until_complete(main_logic(target))
        # break
    # except Exception as e:
    #     print(e)
    except websockets.exceptions.InvalidStatusCode as e:
        pass
    except ssl.SSLCertVerificationError as e:
        pass
    except websockets.exceptions.InvalidMessage as e:
        pass
    except OSError as e:
        pass
    except websockets.exceptions.InvalidURI as e:
        pass