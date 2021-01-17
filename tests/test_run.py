import asyncio
from hkube_debbuging_python_api import Builder, algorithm
import time


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

def test_run_two_nodes():
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