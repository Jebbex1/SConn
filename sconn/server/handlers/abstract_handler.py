from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, create_default_context, TLSVersion, Purpose
from ..setting_parser import get_setting


def tls_wrap_socket(client_socket: socket) -> SSLSocket:
    tls_context = create_default_context()
    tls_context.load_cert_chain(certfile=get_setting("certificate_path"), keyfile=get_setting("certificate_key_path"))
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(client_socket)


class AbstractHandler(ABC):
    def __init__(self, client_socket: socket) -> None:
        super().__init__()
        self.client_socket = tls_wrap_socket(client_socket)
        

        
        
        
        