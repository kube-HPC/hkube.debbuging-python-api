from events import Events


class Algorithm():
    def __init__(self, pipline, name):
        self.events = Events()
        self._pipeline = pipline
        self._callback = None
        self._algorithmName = name
        self._nodeName = name
        self._input=[]


    def runAlgorithm(self, data):
        func = self._callback
        if func:
            return func(data)
        return None

    def input(self, data):
        self._input.append(data)
        return self

    def inputAsBatch(self, data):
        self._input.append('#'+data)

    def add(self, callback):
        instance={
            'algorithmName': self._algorithmName,
            'input': self._input,
            'nodeName': self._nodeName
        }
        self._pipeline.pipeline['nodes'].append(instance)
        self._callback = callback
        self.events.emit_algorithm_register({"name": self._algorithmName})
        return self._pipeline
