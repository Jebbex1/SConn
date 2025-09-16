from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from os.path import exists
from .setting_parser import SETTINGS_YAML_PATH, create_default_settings_yaml, get_setting
from ..protocol.constants import ConnectionTypes
from .handlers.abstract_handler import AbstractHandler
from .handlers.server_client_handler import ServerClientHandler


class Server:
    def __init__(self, connection_type: int) -> None:
        if not exists(SETTINGS_YAML_PATH):
            create_default_settings_yaml()
            
        self.skt = socket(AF_INET, SOCK_STREAM)
        self.skt.bind(('0.0.0.0', get_setting("port")))
        
        match connection_type:
            case _:
                self.handler_class = ServerClientHandler
    
    
    def start(self) -> None:
        self.skt.listen()
        while True:
            client_skt, addr = self.skt.accept()
            subprocess = Process(target=self.handler_class, args=(client_skt,))
            subprocess.start()
        
                                
