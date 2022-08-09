from events import Events
import threading
import time
from hkube_debbuging_python_api.hkube_api_mock import hkube_api as hkube_api_mock


class Algorithm():
    def __init__(self, pipline, name):
        self.events = Events()
        self._pipeline = pipline
        self._callback = None
        self._algorithmName = name
        self._nodeName = name
        self._input = []
        self.hkube_api = hkube_api_mock(pipline, self)
        self.listeners = []
        self.error = None
        self.hkubeApi = None
        self.options = None

    def getNodeName(self):
        return self._nodeName

    def getAlgorithmName(self):
        return self._algorithmName

    def runAlgorithmAsync(self, data):
        func = self._callback
        if func:
            threading.Thread(target=func, args=(data, self.hkube_api)).start()

    def runAlgorithm(self, data):
        func = self._callback
        if func:
            return func(data, self.hkube_api)
        raise Exception('No function was set in algorithm')

    def input(self, data):
        self._input.append(data)
        return self

    def inputAsBatch(self, data):
        self._input.append('#' + data)

    def add(self, callback):
        instance = {
            'algorithmName': self._algorithmName,
            'input': self._input,
            'nodeName': self._nodeName
        }
        if callback.__code__.co_argcount == 1:
            self._callback = lambda args, api: callback(args)
        else:
            self._callback = callback
        self._pipeline.pipeline['nodes'].append(instance)
        self.events.emit_algorithm_register({"name": self._algorithmName})
        return self._pipeline

    def addAsStateless(self, callback):
        algorithm = self
        instance = {
            'algorithmName': self._algorithmName,
            'input': self._input,
            'nodeName': self._nodeName
        }
        # OnMessage insert the message to streaminput in options the stateless gets and invoke the stateless
        def _invokeAlgorithm(msg, origin):
            options = {}
            options.update(algorithm.options)
            options['streamInput'] = {'message': msg, 'origin': origin}
            try:
                result = callback(options, algorithm.hkubeApi)
                algorithm.hkubeApi.sendMessage(result)
            except Exception as e:
                print('statelessWrapper error, ' + str(e))
                algorithm.error = e

        def start(options, hkubeApi):
            # pylint: disable=unused-argument
            algorithm.hkubeApi = hkubeApi
            algorithm.hkubeApi.registerInputListener(onMessage=_invokeAlgorithm)
            algorithm.hkubeApi.startMessageListening()
            algorithm.options = options
            while (self._pipeline.active):
                if (algorithm.error is not None):
                    raise algorithm.error  # pylint: disable=raising-bad-type
                time.sleep(1)

        self._pipeline.pipeline['nodes'].append(instance)
        self._callback = start
        self.events.emit_algorithm_register({"name": self._algorithmName})
        return self._pipeline
