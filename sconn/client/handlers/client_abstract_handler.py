from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_CLIENT
from ...utils.setting_parser import get_setting


def tls_wrap_client_side_socket(skt: socket) -> SSLSocket:
    tls_context = SSLContext(PROTOCOL_TLS_CLIENT)
    tls_context.load_verify_locations(get_setting("ca_certificate_path"))
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(skt)


class ClientAbstractHandler(ABC):
    def __init__(self, skt: socket) -> None:
        super().__init__()
        self.socket = tls_wrap_client_side_socket(skt)
        
    @abstractmethod
    def send(self, data: bytes) -> None:
        pass
            
    @abstractmethod
    def recv(self, buffer_len: int = 1024, flags: int = 0) -> bytes:
        pass