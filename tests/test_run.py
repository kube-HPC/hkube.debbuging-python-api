import asyncio
import time
from hkube_debbuging_python_api import Builder
global gotStreamingMessage
gotStreamingMessage = False

def test1(data):
    print(data['input'])
    return data['input']


def test2(data):
    print(data['input'])
    return data['input']


def test_run():
    class runBuilder():
        async def run():
            build = Builder()
            pipe = await build.createPipeline("test")
            pipe.algorithm("test").input(5).input('@flowInput').add(test1).flowInput().input({"david": 5}).add()
            assert len(pipe.pipeline['nodes']) == 1
            assert pipe.pipeline['nodes'][0]['nodeName'] == 'test'
            assert pipe.pipeline['nodes'][0]['algorithmName'] == 'test'
            assert pipe.pipeline['flowInput'] == {"david": 5}
            return await pipe.execute()
    res = asyncio.run(runBuilder.run())
    assert len(res) == 1
    assert res[0]['nodeName'] == 'test'
    assert res[0]['result'][0] == 5
    assert res[0]['result'][1] == {"david": 5}

def test_run_two_nodes_parallel():
    class runBuilder():
        async def run():
            build = Builder()
            pipe = await build.createPipeline("test1")
            pipe.algorithm("p2_test").input(10).input('@flowInput').add(test1)\
                .algorithm('p2_test2').input(15).input('@flowInput').add(test2)\
                .flowInput().input({"david": 5}).add()
            assert len(pipe.pipeline['nodes']) == 2
            assert pipe.pipeline['nodes'][0]['nodeName'] == 'p2_test'
            assert pipe.pipeline['nodes'][0]['algorithmName'] == 'p2_test'
            assert pipe.pipeline['nodes'][1]['nodeName'] == 'p2_test2'
            assert pipe.pipeline['nodes'][1]['algorithmName'] == 'p2_test2'
            assert pipe.pipeline['flowInput'] == {"david": 5}
            return await pipe.execute()
    res = asyncio.run(runBuilder.run())
    assert len(res) == 2
    assert res[0]['nodeName'] == 'p2_test'
    assert res[0]['result'][0] == 10
    assert res[0]['result'][1] == {"david": 5}
    assert res[1]['nodeName'] == 'p2_test2'
    assert res[1]['result'][0] == 15
    assert res[1]['result'][1] == {"david": 5}

def test_run_two_nodes_serial():
    class runBuilder():
        async def run():
            build = Builder()
            pipe = await build.createPipeline("test1")
            pipe.algorithm("p2_test").input(10).input('@flowInput').add(test1)\
                .algorithm('p2_test2').input(15).input('@p2_test').add(test2)\
                .flowInput().input({"david": 5}).add()
            assert len(pipe.pipeline['nodes']) == 2
            assert pipe.pipeline['nodes'][0]['nodeName'] == 'p2_test'
            assert pipe.pipeline['nodes'][0]['algorithmName'] == 'p2_test'
            assert pipe.pipeline['nodes'][1]['nodeName'] == 'p2_test2'
            assert pipe.pipeline['nodes'][1]['algorithmName'] == 'p2_test2'
            assert pipe.pipeline['flowInput'] == {"david": 5}
            return await pipe.execute()
    res = asyncio.run(runBuilder.run())
    assert len(res) == 1
    assert res[0]['nodeName'] == 'p2_test2'
    assert res[0]['result'][0] == 15
    assert res[0]['result'][1] == [10, {'david': 5}]

gotYahoo = False

def test_streaming():

    class runBuilder():
        async def run():

            def test1(data, hkube_api):
                print("test1 invoked----------------------------------------------")
                while (not gotYahoo):
                    time.sleep(0.01)
                    try:
                        hkube_api.sendMessage('Yoohoo', flow="flow1")
                    except Exception as e:
                        print(str(e))

                time.sleep(7)
                print(data['input'])
                return data['input']

            def test2(data, hkube_api):
                print("test2 invoked ---------------------------------------------------")

                def handleMessage(msg, origin):
                    print('At test2 got ' + msg + ' from ' + origin)
                    hkube_api.sendMessage(msg)

                hkube_api.registerInputListener(onMessage=handleMessage)
                hkube_api.startMessageListening()
                while (not gotYahoo):
                    time.sleep(1)
                time.sleep(0.1)
                print(hkube_api.get_streaming_statistics())
                print('alg2')
                print(data['input'])
                return data['input']

            def test3(data, hkube_api):
                print("test3 invoked ---------------------------------------------------")
                print('At test3 got' + data['streamInput']['message'] + 'from' + data['streamInput']['origin'])
                global gotYahoo
                if not gotYahoo:
                    gotYahoo = True

            build = Builder()
            pipe = await build.createPipeline("test", kind="stream")
            flow = [{"source": "test1", "next": "test2"}, {"source": "test2", "next": "test3"}]
            pipe.setFlows({"flow1": flow})
            pipe.algorithm("test1").input(5).add(test1).algorithm('test2').add(test2).algorithm('test3').addAsStateless(test3).execute()
            time.sleep(1)
            pipe.stop()
            build.ws.stopWS()
        # assert len(pipe.pipeline['nodes']) == 3

    res = asyncio.run(runBuilder.run())
    time.sleep(3)
    global gotYahoo
    assert gotYahoo