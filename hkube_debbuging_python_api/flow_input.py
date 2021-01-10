from hkube_debbuging_python_api.singleton import Singleton


class FlowInput(metaclass=Singleton):
    def __init__(self):
        self.ws = None
        self._pipelineInstance = None
        self.instance = {}

    def _clear(self):
        self._pipelineInstance = None

    def init(self, piplineInstance):
        self._pipelineInstance = piplineInstance
        self.instance = {}
        return self

    def input(self, data):
        self.instance.update(data)
        return self

    def inputAll(self, data):
        self.instance = data
        return self

    def add(self):
        self._pipelineInstance.pipeline['flowInput'] = self.instance
        return self._pipelineInstance
