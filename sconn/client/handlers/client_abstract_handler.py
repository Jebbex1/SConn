from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_CLIENT
from ...utils.setting_parser import get_setting


def tls_wrap_client_side_socket(skt: socket) -> SSLSocket:
    """Wraps the client-side socket with TLS 1.3

    :param skt: he socket to wrap.
    :type skt: socket
    :return: The TLS 1.3 wrapped socket.
    :rtype: SSLSocket
    """
    tls_context = SSLContext(PROTOCOL_TLS_CLIENT)
    tls_context.load_verify_locations(get_setting("ca_certificate_path"))
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(skt, server_hostname=get_setting("server_hostname"))


class ClientAbstractHandler(ABC):
    """An abstract class that is initialized with every connection with inheritance, is in charge of wrapping the connection with TLS 1.3.
    """
    def __init__(self, skt: socket) -> None:
        """Initializes the base ClientAbstractHandler instance, and wraps the connection of `skt` with TLS 1.3

        :param skt: The socket to wrap
        :type skt: socket
        """
        super().__init__()
        self.socket = tls_wrap_client_side_socket(skt)
        
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
