from socket import socket, AF_INET, SOCK_STREAM
from os.path import exists
from .handlers.client_abstract_handler import ClientAbstractHandler
from .handlers.client_sc_model_handler import ClientSCModelHandler
from ..utils.setting_parser import CLIENT_CONFIG_PATH, create_default_config, get_setting
from ..protocol.constants import ConnectionTypes

class Client:
    def __init__(self, connection_type: ConnectionTypes) -> None:
        """Initializes the Client object, and creates a default config file if the path for it is empty.

        :param connection_type: A ConnectionTypes enum selection, to specify the model of the connection.
        :type connection_type: ConnectionTypes
        """
        if not exists(CLIENT_CONFIG_PATH):
            create_default_config()
        
        self.handler: ClientAbstractHandler
        self.connection_type = connection_type
        
    def connect(self) -> None:
        """Connects the client to a server.
        """
        skt = socket(AF_INET, SOCK_STREAM)
        skt.connect((get_setting("server_hostname"), get_setting("port")))
        match self.connection_type:
            case _:
                self.handler = ClientSCModelHandler(skt)
    
    def disconnect(self) -> None:
        """Effectively disconnects the client from the server, by closing its socket.
        """
        self.handler.socket.close()
        
    def send(self, data: bytes) -> None:
        """Sends data to the server by using the client-side handler's send() function.

        :param data: The data to send.
        :type data: bytes
        """
        self.handler.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        """Receives data from the server connection by using the handler's recv() function.

        :param buffer_len: The maximum amount of bytes to receive at once, defaults to 1024
        :type buffer_len: int, optional
        :param flags: The flags to be passed into the socket.recv() function, defaults to 0
        :type flags: int, optional
        :return: A bytes object that represents the data received.
        :rtype: bytes
        """
        return self.handler.recv(buffer_len, flags)
