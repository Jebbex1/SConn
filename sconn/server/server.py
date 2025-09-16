from socket import socket, AF_INET, SOCK_STREAM
from multiprocessing import Process
from threading import Thread
from os.path import exists
from functools import partial
from .setting_parser import SETTINGS_YAML_PATH, create_default_settings_yaml, get_setting
from .handlers.server_client_handler import ServerClientHandler
from ..protocol.constants import ConnectionTypes


class Server:
    def __init__(self, connection_type: int, 
                 handler_exit_function: partial | None = None) -> None:
        """Initializes the Server object.

        :param connection_type: An ConnectionTypes enum selection, to specify the model of the connection.
        :type connection_type: int
        :param handler_exit_function: If the handler interacts with the client directly after the initial handshake 
         (e.g. a Server-Client Model), we need to route the process to the function that does that, this parameter is that function. 
         Defaults to None.
        :type handler_exit_function: partial | None, optional
        """

        if not exists(SETTINGS_YAML_PATH):
            create_default_settings_yaml()
            
        self.skt = socket(AF_INET, SOCK_STREAM)
        self.skt.bind(('0.0.0.0', get_setting("port")))
        
        self.handler_exit_function = handler_exit_function
        
        match connection_type:
            case _:
                self.handler_class = ServerClientHandler
        
        self.listening_thread = Thread(target=self._start_listening)
                
    def _start_listening(self) -> None:
        self.skt.listen()
        try:
            while True:
                client_skt, addr = self.skt.accept()
                if self.handler_exit_function is not None:
                    subprocess = Process(target=self.handler_class, args=(client_skt, self.handler_exit_function))
                else:
                    subprocess = Process(target=self.handler_class, args=(client_skt,))
                subprocess.start()
        except OSError:  # self.stop() was called
            return
    
    
    def start(self) -> None:
        self.listening_thread.start()
    
    
    def stop(self) -> None:
        self.skt.close()
