import asyncio
from lib.pipeline import Pipeline
import lib.algorithm
import threading
from lib.wcClient import WebsocketClient


class Builder():
    def __init__(self):
        self.wsReady = False

    def config(self):
        self.loop = asyncio.get_running_loop()
        self.future = self.loop.create_future()
        self.ws = WebsocketClient()
        self.ws.events.on_connection += self.onConnect
        t = threading.Thread(target=self.ws.startWS,
                             args=("ws://localhost:3060",))
        t.start()
        return self.future

    def onConnect(self):
        self.wsReady = True
        self.loop.call_soon_threadsafe(self.future.set_result, 4)
        # self.future.set_result(50)

    async def createPipeline(self, name):
        if self.wsReady == False:
            await self.config()
            return Pipeline()._init(name)

    # async def createPipeline1(self, name):
    #         if self.wsReady == False:
    #             await self.config()
    #             print('im here')
    #             return pipeline._init(name)
    # async def createPipeline:
    #     await
