from functools import partial
from sconn.server.server import Server
from sconn.client.client import Client
from sconn.protocol.constants import ConnectionModels
from ssl import SSLSocket
from sconn.utils.config_interface import ServerConfig


def reply_with_sent_once(skt: SSLSocket, config: ServerConfig) -> None:
    skt.send(skt.recv())


def test_sc_model_regular() -> None:
    server = Server(config_path =           "testing_server_config.yaml", 
                    handler_exit_function = partial(reply_with_sent_once))
    server.start()
    
    
    client = Client(ConnectionModels.SERVER_CLIENT,
                    config_path="testing_client_config.yaml")
    client.connect()
    
    data = b"WAAAAAAAAAAAAA"
    client.send(data)
    assert client.recv() == data
    
    client.disconnect()
    server.stop()


def test_sc_model_mtls() -> None:
    server = Server(config_path =           "testing_mtls_server_config.yaml", 
                    handler_exit_function = partial(reply_with_sent_once))
    server.start()
    
    
    client = Client(ConnectionModels.SERVER_CLIENT,
                    config_path="testing_mtls_client_config.yaml")
    client.connect()
    
    data = b"WAAAAAAAAAAAAA"
    client.send(data)
    assert client.recv() == data
    
    client.disconnect()
    server.stop()