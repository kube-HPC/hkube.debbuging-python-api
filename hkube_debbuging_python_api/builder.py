import asyncio
from hkube_debbuging_python_api.pipeline import Pipeline
from hkube_debbuging_python_api.wcClient import WebsocketClient
import threading


class Builder():
    def __init__(self):
        self.wsReady = False
        self.loop = None
        self.future = None
        self.ws = None

    def config(self):
        self.loop = asyncio.get_running_loop()
        self.future = self.loop.create_future()
        self.ws = WebsocketClient()
        self.ws.events.on_connection += self.onConnect
        # TODO: move ws connect string to config/params
        t = threading.Thread(target=self.ws.startWS, args=("ws://localhost:3060",))
        t.start()
        return self.future

    def onConnect(self):
        self.wsReady = True
        self.loop.call_soon_threadsafe(self.future.set_result, 4)

    async def createPipeline(self, name, kind='batch'):
        if not self.wsReady:
            await self.config()
        return Pipeline(name, self.ws, kind)
