from hkube_debbuging_python_api.consts import fields

class FlowInput():
    def __init__(self, pipline):
        self._pipline = pipline
        self.instance = {}

    def input(self, data):
        self.instance.update(data)
        return self

    def inputAll(self, data):
        self.instance = data
        return self

    def add(self):
        self._pipline.pipeline[fields.flowInput] = self.instance
        return self._pipline
