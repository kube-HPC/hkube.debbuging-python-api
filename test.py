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


class runBuilder():

    async def run():
        build = Builder()
        pipe = await build.createPipeline("test")
        pipe.algorithm("test").input(5).add(test1)\
        .algorithm('test1').input("@test").input(8).add(test1)\
        .algorithm("test2").input("@test1").add(test2)\
        .flowInput().input({"david": 5}).add()
        return await pipe.execute()


bla = asyncio.run(runBuilder.run())
print('finish', bla)
