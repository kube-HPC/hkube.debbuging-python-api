import websocket
import simplejson as json
from hkube_debbuging_python_api.algorithm import Algorithm
from hkube_debbuging_python_api.pipeline import Pipeline
from events import Events
import time


class WebsocketClient:
    def __init__(self):
        self.events = Events()
        self._ws = None
        self._reconnectInterval = 5
        self._active = True
        self._switcher = {
            "RUN_ALGORTIHM": self.runAlgorithm,
            "PIPELINE_CREATED": self.pipelineExecute,
            "PIPELINE_FINISHED": self.pipelineDone,
        }
        self.algorithm = Algorithm()
        self.pipeline = Pipeline()
        self.algorithm.events.emit_algorithm_register += self.algorithmRegister
        self.pipeline.events.emit_pipeline_create += self.pipelineCreate

    def algorithmRegister(self, data):
        self.send('ALGORITHM_REGISTER', {"name": data["name"]})

    def runAlgorithm(self, data):
        result = None
        try:
            result = self.algorithm.runAlgorithm(data['algorithmName'], data)

           # res = result == None if {} else result
            self.send("ALGORTIHM_FINISHED_SUCCESS", {
                      "data": data, "result": result or {}})
        except Exception:
            self.send("ALGORTIHM_FINISHED_FAILED", {
                      "data": data, "result": result or {}})

    def pipelineCreate(self, data):
        self.send("PIPELINE_CREATE", data)

    def pipelineExecute(self,_):
        self.send("PIPELINE_EXECUTE", {})

    def pipelineDone(self, data):
        print('pipelineDone', data)
        self.pipeline.done(data)
        self.stopWS()

    def stop(self, data):
        self.events.on_stop(data)

    def exit(self, data):
        self.events.on_exit(data)

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
        self.events.on_disconnect()

    def on_open(self):
        self.events.on_connection()

    def send(self, type, message):
      #      print(f'sending message to worker: {type}')
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
