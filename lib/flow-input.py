
class flowInput():
    def __init__(self):
        self.ws = None
        self._pipelineInstance = None

    def _clear(self):
        self.instance = {}
        self._pipelineInstance = None

    def _init(self, piplineInstance):
        self._pipelineInstance = piplineInstance
        self.instance = {}

    def input(self, data):
        self.instance.update(data)
        return self

    def inputAll(self, data):
        self.instance = data
        return self

    def add(self):
        self._pipelineInstance._pipline.flowInput = self.instance
        return self._pipelineInstance
