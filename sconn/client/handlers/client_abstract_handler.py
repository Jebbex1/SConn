from abc import ABC, abstractmethod
from ssl import SSLSocket
from ...utils.config_interface import ClientConfig


class ClientAbstractHandler(ABC):
    """An abstract class that is initialized with every connection with inheritance, is in charge of wrapping the connection with TLS 1.3.
    """
    def __init__(self, skt: SSLSocket, config: ClientConfig) -> None:
        """Initializes the base ClientAbstractHandler instance, and wraps the connection of `skt` with TLS 1.3

        :param skt: The socket to wrap
        :type skt: socket
        """
        super().__init__()
        self.config = config
        self.socket = skt

    @abstractmethod
    def send(self, data: bytes) -> None:
        """An abstract method that requires to be implemented with every child class of ClientAbstractHandler. 
         The purpose of the implemented function is to send data to the server.

        :param data: The data to send.
        :type data: bytes
        """
        pass

    @abstractmethod
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        """An abstract method that requires to be implemented with every child class of ClientAbstractHandler.
         The purpose of the implemented function is to receive data from the server.

        :param buffer_len: The maximum amount of bytes to receive at once, defaults to 1024
        :type buffer_len: int, optional
        :param flags: The flags to be passed into the socket.recv() function, defaults to 0
        :type flags: int, optional
        :return: A bytes object that represents the data received.
        :rtype: bytes
        """
        pass
