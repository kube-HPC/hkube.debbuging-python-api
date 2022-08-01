class hkube_api:
    def __init__(self, pipeline, algo):
        self.hasStartedListeningToMessages = False
        self.pipeline = pipeline
        self.currentAlgorithm = algo

    def registerInputListener(self, onMessage):
        self.currentAlgorithm.listeners.append(onMessage)

    def startMessageListening(self):
        self.hasStartedListeningToMessages = True

    def sendMessage(self, msg, flow=None):
        next = self._getNextNode(flow)
        if next is not None:
            nextAlgo = self.pipeline.getAlgorithm(next)
            for listener in nextAlgo.listeners:
                listener(msg, self.currentAlgorithm.getNodeName())

    def _getNextNode(self, flowName):
        if flowName is None:
            flowName = self.pipeline.getDefaultFlow()
        currentFlow = self.pipeline.getFlow(flowName).copy()
        for node in currentFlow:
            if node['source'] == self.currentAlgorithm.getAlgorithmName():
                current = node
                return current['next']
        return None

    def stopStreaming(self, force=True):
        pass

    def isListeningToMessages(self):
        return True

    def get_streaming_statistics(self):
        return {"statisticsPerNode": [{"nodeName": "NextNodeName", "sent": -1, "queueSize": -1, "dropped": -1}], "binarySize": -1, "configuredMaxBinarySize": -1}

    def dataSourceResponse(self, data):
        pass

    def start_algorithm(self, algorithmName, input=[], includeResult=True):
        pass

    def getDataSource(self, dataSource):
        pass

    def start_stored_subpipeline(self, name, flowInput={}, includeResult=True):
        pass

    def start_raw_subpipeline(self, name, nodes, flowInput, options={}, webhooks={}, includeResult=True):
        pass

    def resetQueue(self):
        pass

    def resetQueuePartial(self, numberOfMessagesToRemove):
        pass

    def _waitForResult(self, execution):
        pass
