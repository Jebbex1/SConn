from socket import socket
from .client_abstract_handler import ClientAbstractHandler


class ClientSCModelHandler(ClientAbstractHandler):
    """The client-side class to manage the simplest connection model; the Server-Client model. Extends `ClientAbstractHandler`.
    """
    def __init__(self, skt: socket, config_path: str) -> None:
        """Initializes the instance of this class. Firstly wraps the connection with TLS 1.3 via ClientAbstractHandler's constructor

        :param skt: The socket to wrap and send data through. This socket is connected to the server.
        :type skt: socket
        """
        super().__init__(skt, config_path)
    
    def send(self, data: bytes) -> None:
        """Sends data to the server.

        :param data: The data to send.
        :type data: bytes
        """
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