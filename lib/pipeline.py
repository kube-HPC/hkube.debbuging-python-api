from lib.algorithm import Algorithm
from events import Events
from lib.singleton import Singleton


class Pipeline(metaclass=Singleton):
    def __init__(self):
        self.ws = None
        self.events = Events()
        self._pipeline = {
            "name": '',
            "nodes": [],
            "flowInput": []
        }

    def _init(self, name):
        self.event = Events()
        self._pipeline = {
            "name": name,
            "nodes": [],
            "flowInput": []
        }
        return self

    def algorithm(self, name):
        return Algorithm()._init(self, name)

    def flowInput(self):
        return

    def execute(self):
        self.events.emit_pipeline_create({"pipeline": self._pipeline})
