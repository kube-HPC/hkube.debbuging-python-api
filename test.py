import asyncio
from hkube_debbuging_python_api import Builder


def test1(data):
    print(data['input'])
    return data['input'][0]


def test2(data):
    print(data['input'])
    return data['input']


class runBuilder():

    async def run():
        build = Builder()
        pipe = await build.createPipeline("test")
        pipe.algorithm("test").input(5).add(test1).algorithm(
            'test2').input("@test").input(8).add(test1).algorithm("test5").input("@test2").add(test2).flowInput().input({"david": 5}).add().execute()


bla = asyncio.run(runBuilder.run())
print('finish')
