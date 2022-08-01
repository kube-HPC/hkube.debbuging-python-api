from abc import abstractmethod


class Communication:
    @property
    @abstractmethod
    def events(self):
        pass

    @abstractmethod
    def algorithmRegister(self, data):
        pass

    @abstractmethod
    def setAlgorithmResult(self, result):
        pass

    @abstractmethod
    def pipelineCreate(self, data):
        pass

    @abstractmethod
    def pipelineExecute(self, _):
        pass

    @abstractmethod
    def pipelineDone(self, data):
        pass
