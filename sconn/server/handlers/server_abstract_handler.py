from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_SERVER
from ...utils.setting_parser import get_setting


def tls_wrap_server_side_socket(skt: socket) -> SSLSocket:
    """Wraps the server-side socket with TLS 1.3

    :param skt: The socket to wrap, this socket is the one connected to the client.
    :type skt: socket
    :return: The TLS 1.3 wrapped socket.
    :rtype: SSLSocket
    """
    tls_context = SSLContext(PROTOCOL_TLS_SERVER)
    tls_context.load_cert_chain(certfile=get_setting("certificate_path",     server_side=True), 
                                keyfile= get_setting("certificate_key_path", server_side=True))
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(skt, server_side=True)


class ServerAbstractHandler(ABC):
    """An abstract class that is initialized with every connection with inheritance, is in charge of wrapping the connection with TLS 1.3.
    """
    def __init__(self, skt: socket) -> None:
        """Initializes the base ServerAbstractHandler instance, and wraps the connection of `skt` with TLS 1.3

        :param skt: The socket to wrap
        :type skt: socket
        """
        super().__init__()
        self.socket = tls_wrap_server_side_socket(skt)
