from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_SERVER
from ...utils.config_interface import ServerConfig


def tls_wrap_server_side_socket(skt: socket, config: ServerConfig) -> SSLSocket:
    """Wraps the server-side socket with TLS 1.3

    :param skt: The socket to wrap, this socket is the one connected to the client.
    :type skt: socket
    :return: The TLS 1.3 wrapped socket.
    :rtype: SSLSocket
    """
    tls_context = SSLContext(PROTOCOL_TLS_SERVER)
    certfile_path, keyfile_path = config.get_tls_certificate_paths()
    tls_context.load_cert_chain(certfile=certfile_path, 
                                keyfile =keyfile_path)
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(skt, server_side=True)


class ServerAbstractHandler(ABC):
    """An abstract class that is initialized with every connection with inheritance, is in charge of wrapping the connection with TLS 1.3.
    """
    def __init__(self, skt: socket, config_path: str) -> None:
        """Initializes the base ServerAbstractHandler instance, and wraps the connection of `skt` with TLS 1.3

        :param skt: The socket to wrap
        :type skt: socket
        """
        super().__init__()
        self.config = ServerConfig(config_path)
        self.socket = tls_wrap_server_side_socket(skt, self.config)
