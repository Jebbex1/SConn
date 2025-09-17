from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_SERVER
from ...setting_parser import get_setting


def tls_wrap_socket(client_socket: socket) -> SSLSocket:
    tls_context = SSLContext(PROTOCOL_TLS_SERVER)
    tls_context.load_cert_chain(certfile=get_setting("certificate_path"), keyfile=get_setting("certificate_key_path"))
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(client_socket, server_side=True)


class AbstractHandler(ABC):
    def __init__(self, client_socket: socket) -> None:
        super().__init__()
        self.client_socket = tls_wrap_socket(client_socket)
