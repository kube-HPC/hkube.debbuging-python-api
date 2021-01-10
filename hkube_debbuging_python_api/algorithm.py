from events import Events
from hkube_debbuging_python_api.singleton import Singleton


class Algorithm(metaclass=Singleton):
    def __init__(self):
        self.ws = None
        self.events = Events()
        self._pipelineInstance = None
        self._registerAlgorithm = {}
        self.instance = {}

    def _clear(self):
        self.instance = {}
        self._registerAlgorithm = {}
        self._pipelineInstance = None

    def init(self, piplineInstance, name):
        self._pipelineInstance = piplineInstance
        self.instance = {"nodeName": name, "input": [], "algorithmName": name}
        return self

    def registerAlgorithm(self, algorithm_name, algorithm):
        self._registerAlgorithm[algorithm_name] = algorithm

    def input(self, data):
        self.instance['input'].append(data)
        return self

    def inputAsBatch(self, data):
        self.instance.input.append('#'+data)

    def inputArray(self, data):
        self.instance = data
        return self

    def add(self, callback):
        self._pipelineInstance.pipeline['nodes'].append(self.instance)
        self._registerAlgorithm[self.instance['algorithmName']] = callback
        self.events.emit_algorithm_register(
            {"name": self.instance['algorithmName']})
        return self._pipelineInstance