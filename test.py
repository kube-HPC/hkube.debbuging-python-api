import asyncio
from lib.builder import Builder


def test1(data):
    print(data['input'])
    return data['input']


class runBuilder():

    async def run():
        build = Builder()
        pipe = await build.createPipeline("test")
        pipe.algorithm("test").input(5).add(test1).algorithm(
            'test2').input("@test").add(test1).execute()


bla = asyncio.run(runBuilder.run())
print('finish')
