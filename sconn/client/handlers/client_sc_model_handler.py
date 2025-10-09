from ssl import SSLSocket
from .client_abstract_handler import ClientAbstractHandler
from ...utils.config_interface import ClientConfig


class ClientSCModelHandler(ClientAbstractHandler):
    def __init__(self, skt: SSLSocket, config: ClientConfig) -> None:
        super().__init__(skt, config)
    
    def send(self, data: bytes) -> None:
        self.socket.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        """Receives data from the server connection.

        :param buffer_len: The maximum amount of bytes to receive at once, defaults to 1024
        :type buffer_len: int, optional
        :param flags: The flags to be passed into the socket.recv() function, defaults to 0
        :type flags: int, optional
        :return: A bytes object that represents the data received.
        :rtype: bytes
        """
        return self.socket.recv(buffer_len, flags)
