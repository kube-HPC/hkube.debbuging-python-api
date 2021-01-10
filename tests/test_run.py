import asyncio
from hkube_debbuging_python_api import Builder
import time


def test1(data):
    print(data['input'])
    return data['input'][0]


def test2(data):
    print(data['input'])
    time.sleep(2)
    return data['input']


def test_run():
    class runBuilder():
        async def run():
            build = Builder()
            pipe = await build.createPipeline("test")
            pipe.algorithm("test").input(5).add(test1)
            future = pipe.execute()
            assert future
            res = await future
            return res
    res = asyncio.run(runBuilder.run())
    assert len(res) == 1
    assert res[0]['nodeName'] == 'test2'