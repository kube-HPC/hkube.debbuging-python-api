import websocket
import simplejson as json
from hkube_debbuging_python_api.consts import messages
from hkube_debbuging_python_api.communication import Communication
from events import Events
import time


class WebsocketClient(Communication):
    def __init__(self):
        self._events = Events()
        self._ws = None
        self._reconnectInterval = 5
        self._active = True
        self._switcher = {
            messages.RUN_ALGORTIHM: self._events.on_run_algorithm,
            messages.PIPELINE_CREATED: self.pipelineExecute,
            messages.PIPELINE_FINISHED: self.pipelineDone,
        }

    @property
    def events(self):
        return self._events

    def algorithmRegister(self, data):
        self.send(messages.ALGORITHM_REGISTER, {"name": data["name"]})

    def setAlgorithmResult(self, data, result):
        self.send(messages.ALGORTIHM_FINISHED_SUCCESS, {"data": data, "result": result or {}})

    def pipelineCreate(self, data):
        self.send(messages.PIPELINE_CREATE, data)

    def pipelineExecute(self,_):
        self.send(messages.PIPELINE_EXECUTE, {})

    def pipelineDone(self, data):
        self._events.on_pipeline_done(data)
        self.stopWS()

    def stop(self, data):
        self._events.on_stop(data)

    def exit(self, data):
        self._events.on_exit(data)

    def on_message(self, message):
        decoded = json.loads(message)
        command = decoded["type"]
        print(f'got message from worker: {command}')
        func = self._switcher.get(command)
        if not func:
            return
        data = decoded.get("data", None)
        func(data)

    def on_error(self, error):
        print(error)

    def on_close(self):
        self._events.on_disconnect()

    def on_open(self):
        self._events.on_connection()

    def send(self, type, message):
        self._ws.send(json.dumps({"type": type, "data": message}))

    def startWS(self, url):
        self._ws = websocket.WebSocketApp(
            url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close)
        while self._active:
            try:
                self._ws.run_forever()
                if not self._active:
                    break
                time.sleep(self._reconnectInterval)
            except Exception:
                pass

    def stopWS(self):
        self._active = False
        if self._ws:
            self._ws.close()
