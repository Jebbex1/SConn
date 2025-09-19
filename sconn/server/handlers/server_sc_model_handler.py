from socket import socket
from functools import partial
from .server_abstract_handler import ServerAbstractHandler


class ServerSCModelHandler(ServerAbstractHandler):
    """The server-side class to manage the simplest connection model; the Server-Client model. Extends `ServerAbstractHandler`.
    """
    def __init__(self, skt: socket, exit_function: partial) -> None:
        """Initializes the instance of this class. Firstly wraps the connection with TLS 1.3 via ServerAbstractHandler's constructor

        :param skt: The socket to wrap and send data through. This socket is connected to a client.
        :type skt: socket
        :param exit_function: Because each client is managed in its own process, we need to patch through a function that will be called at the end of object creation, 
         so we can continue to communicate with that client from the managing process. This function must have a key word argument `handler` that will represent the 
         handler object of the connection
        :type exit_function: partial
        """
        super().__init__(skt)
        self.exit_function = exit_function
        exit_function(handler=self)
    
    def send(self, data: bytes) -> None:
        """Sends data through the connection.

        :param data: The data to send.
        :type data: bytes
        """
        self.socket.send(data)
    
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        """Receives data through the connection.

        :param buffer_len: The maximum amount of bytes to receive at once, defaults to 1024
        :type buffer_len: int, optional
        :param flags: The flags to be passed into the socket.recv() function, defaults to 0
        :type flags: int, optional
        :return: A bytes object that represents the data received.
        :rtype: bytes
        """
        return self.socket.recv(buffer_len, flags)
