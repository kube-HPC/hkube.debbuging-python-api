from websocket_server import WebsocketServer
import json 

class WebSocketServerClass:
    def __init__(self, server):
        self._server = server
        self._server.set_fn_new_client(self.handleConnected)
        self._server.set_fn_client_left(self.handleDisconnected)
        self._server.set_fn_message_received(self.handleMessage)
        algos={
            'current': 0,
            'order': [
                {'algorithmName':'test', 'input': [1,2,3]}
            ]
        }
        def nextAlgo(client):
            if (algos['current']>=len(algos['order'])):
                self.sendMsgToClient(client, {'type': 'PIPELINE_FINISHED', 'data': [{'nodeName': 'test', 'algorithmName': 'test', 'result': {'foo': 2}}]})
                return False
            self.sendMsgToClient(client, {'type': 'RUN_ALGORTIHM', 'data': algos['order'][algos['current']]})
            algos['current']+=1
            return True

        self._commands = {
            "PIPELINE_CREATE":  {
                'type': "PIPELINE_CREATED",
                'data': lambda data: None
            },
            "PIPELINE_EXECUTE":  {
                'type': "PIPELINE_EXECUTED",
                'data': lambda data: None,
                'after': nextAlgo
            },
            "ALGORITHM_REGISTER":  {
                'type': "ALGORITHM_REGISTERED",
                'data': lambda data: None
            },
            "ALGORTIHM_FINISHED_SUCCESS":  {
                'after': nextAlgo
            },
            "ALGORTIHM_FINISHED_FAILED":  {
                'after': nextAlgo
            }
        }

    def handleMessage(self, client, server, message):
        decoded = json.loads(message)
        command = decoded["type"]
        data = decoded.get("data", None)
        commandBack = self._commands.get(command)
        if(commandBack):
            after = commandBack.get("after", None)
            msgType = commandBack.get("type", None)
            if (msgType):
                msgBack = {
                    "type": msgType,
                    "data": commandBack["data"](data)
                }
                self.sendMsgToClient(client, msgBack)
            if (after):
                after(client)

    def handleConnected(self, client, server):
        # print('ws connected')
        # self.sendMsgToClient(client, {'command': 'initialize', 'data': mockdata.initData})
        pass

    def handleDisconnected(self, client, server):
        # print('ws disconnected')
        # self.close()
        pass

    def sendMsgToClient(self, client, data):
        self._server.send_message(client, json.dumps(data))
    
    def close(self):
        self._server.shutdown()


def startWebSocketServer():
    port = 3060
    server = WebsocketServer(int(port))
    wss = WebSocketServerClass(server)
    server.run_forever()


if __name__ == "__main__":
    startWebSocketServer()
