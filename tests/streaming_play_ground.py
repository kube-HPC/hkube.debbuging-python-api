import asyncio
import time
from hkube_debbuging_python_api.builder import Builder


def test1(data, hkube_api):
    # print(hkube_api)
    print('___')
    while (True):
        time.sleep(1)
        try:
            hkube_api.sendMessage('Yoohoo', flow="flow1")
        except Exception as e:
            print(str(e))

    time.sleep(7)
    print(data['input'])
    return data['input']


def test2(data, hkube_api):
    def handleMessage(msg, origin):
        print('At test2 got ' + msg +' from ' + origin)
        hkube_api.sendMessage(msg)

    hkube_api.registerInputListener(onMessage=handleMessage)
    hkube_api.startMessageListening()
    active = True
    while (active):
        time.sleep(10)
    print('___')
    time.sleep(2)
    print(hkube_api.get_streaming_statistics())
    print('alg2')
    print(data['input'])
    return data['input']

def test3(data,hkube_api):
    print ('At test3 got' + data['streamInput']['message'] + 'from' + data['streamInput']['origin'])


class runBuilder():

    async def run(self, b):
        build = Builder()
        pipe = await build.createPipeline("test",kind="stream")
        flow = [{"source": "test1", "next": "test2"},{"source": "test2", "next": "test3"}]
        pipe.setFlows({"flow1": flow})
        pipe.algorithm("test1").input(5).add(test1).algorithm('test2').add(test2).algorithm('test3').addAsStateless(test3).execute()


bla = asyncio.run(runBuilder().run('b'))
print('finish')
