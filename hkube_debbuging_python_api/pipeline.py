from hkube_debbuging_python_api.algorithm import Algorithm
from hkube_debbuging_python_api.communication import Communication
from hkube_debbuging_python_api.flow_input import FlowInput
from hkube_debbuging_python_api.consts import fields
from events import Events
import asyncio


class Pipeline():
    def __init__(self, name, communication: Communication, kind='batch'):
        self.active = True
        self.ws = None
        self.events = Events()
        self.pipeline = {
            "name": name,
            "kind": kind,
            "nodes": [],
            "flowInput": []
        }
        self._kind = kind
        self.event = None
        self.loop = None
        self.future = None
        self._algorithms = {}
        self.loop = asyncio.get_running_loop()
        self.future = self.loop.create_future()
        self._communication = communication
        self._communication.events.on_pipeline_done += self.done
        self._communication.events.on_run_algorithm += self._run_algorithm
        self._flows = {}  # "flowName":[{"source":"A","next":"B"}],
        self._defaultFlowName = None

    def setFlows(self, flows):
        self._flows = flows

    def getFlow(self, name):
        return self._flows.get(name)

    def setDefaultFlow(self, name):
        self._defaultFlowName = name

    def getDefaultFlow(self):
        if self._defaultFlowName is None:
            if len(list(self._flows.keys())) == 0:
                raise Exception('No flows were defined can not get default flow')
            return list(self._flows.keys())[0]
        return self._defaultFlowName

    def algorithm(self, name):
        algorithm = Algorithm(self, name)
        algorithm.events.emit_algorithm_register += self._algorithmRegister
        self._algorithms[name] = algorithm
        return algorithm

    def _run_algorithm(self, data):
        algorithmName = data['algorithmName']
        if self._kind == 'stream':
            self.getAlgorithm(algorithmName).runAlgorithmAsync(data)
        else:
            result = self.getAlgorithm(algorithmName).runAlgorithm(data)
        self._communication.setAlgorithmResult(data, result)

    def getAlgorithm(self, name):
        return self._algorithms[name]

    def flowInput(self):
        return FlowInput(self)

    def execute(self):
        if self._kind == 'stream' and len(list(self._flows.keys())) == 0:
            raise Exception('No flows were defined for default flow')
        self._communication.pipelineCreate({fields.pipeline: self.pipeline})
        return self.future


    def done(self, data):
        self.loop.call_soon_threadsafe(self.future.set_result, data)

    def stop(self):
        self.active = False

    def _algorithmRegister(self, data):
        self._communication.algorithmRegister(data)# pylint: disable=protected-access
