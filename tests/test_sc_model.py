from functools import partial
from sconn.server.handlers.server_sc_model_handler import ServerSCModelHandler
from sconn.server.server import Server
from sconn.client.client import Client
from sconn.protocol.constants import ConnectionTypes


def reply_with_sent(handler: ServerSCModelHandler) -> None:
    handler.send(handler.recv())


def test_sc_model() -> None:
    server = Server(ConnectionTypes.SERVER_CLIENT, 
                    partial(reply_with_sent))
    server.start()
    client = Client(ConnectionTypes.SERVER_CLIENT)
    client.connect()
    
    data = b"WAAAAAAAAAAAAA"
    client.send(data)
    assert client.recv() == data
    
    client.disconnect()
    server.stop()
