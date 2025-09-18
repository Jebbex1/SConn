from socket import socket, AF_INET, SOCK_STREAM
from os.path import exists
from .handlers.client_abstract_handler import ClientAbstractHandler
from .handlers.client_sc_model_handler import ClientSCModelHandler
from ..utils.setting_parser import CLIENT_CONFIG_PATH, create_default_config, get_setting
from ..protocol.constants import ConnectionTypes

class Client:
    def __init__(self, connection_type: ConnectionTypes) -> None:
        if not exists(CLIENT_CONFIG_PATH):
            create_default_config()
        
        self.handler: ClientAbstractHandler
        self.connection_type = connection_type
        
    def connect(self) -> None:
        skt = socket(AF_INET, SOCK_STREAM)
        skt.connect((get_setting("server_hostname"), get_setting("port")))
        match self.connection_type:
            case _:
                self.handler = ClientSCModelHandler(skt)
    
    def disconnect(self) -> None:
        self.handler.socket.close()
        
    def send(self, data: bytes) -> None:
        self.handler.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        return self.handler.recv(buffer_len, flags)
