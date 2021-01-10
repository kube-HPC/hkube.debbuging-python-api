from hkube_debbuging_python_api.algorithm import Algorithm
from hkube_debbuging_python_api.flow_input import FlowInput
from hkube_debbuging_python_api.singleton import Singleton
from events import Events


class Pipeline(metaclass=Singleton):
    def __init__(self):
        self.ws = None
        self.events = Events()
        self.pipeline = {
            "name": '',
            "nodes": [],
            "flowInput": []
        }
        self.event = None


    def init(self, name):
        self.event = Events()
        self.pipeline = {
            "name": name,
            "nodes": [],
            "flowInput": []
        }
        return self

    def algorithm(self, name):
        return Algorithm().init(self, name)

    def flowInput(self):
        return FlowInput().init(self)

    def execute(self):
        self.events.emit_pipeline_create({"pipeline": self.pipeline})