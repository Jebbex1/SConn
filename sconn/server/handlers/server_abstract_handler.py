from abc import ABC, abstractmethod
from socket import socket
from ssl import SSLSocket, TLSVersion, SSLContext, PROTOCOL_TLS_SERVER
from ...utils.setting_parser import get_setting


def tls_wrap_server_side_socket(skt: socket) -> SSLSocket:
    tls_context = SSLContext(PROTOCOL_TLS_SERVER)
    tls_context.load_cert_chain(certfile=get_setting("certificate_path",     server_side=True), 
                                keyfile= get_setting("certificate_key_path", server_side=True))
    tls_context.minimum_version = TLSVersion.TLSv1_3
    return tls_context.wrap_socket(skt, server_side=True)


class ServerAbstractHandler(ABC):
    def __init__(self, skt: socket) -> None:
        super().__init__()
        self.socket = tls_wrap_server_side_socket(skt)
