import socket as socket

from .communication_errors import TransmissionProtocolError
from .constants import LFS, CHARSET
from .packet_analyzer import PacketInfo
from ..utils.config_interface import BaseConfig


def recv_packet(skt: socket.socket, config: BaseConfig) -> PacketInfo:
    """
    Receives a packet by the transmission protocol, and returns it as a string.
    :param validate_sizes: should the
    :param skt: the socket interface that we can use to communicate
    :return: the received packet
    """
    length = skt.recv(LFS)  # receive packet length
    if not length.decode().isnumeric():
        raise TransmissionProtocolError(f"Socket at address {skt.getsockname()[0]}:{str(skt.getsockname()[1])} sent a "
                                        f"packet that doesn't follow the transmission protocol")
    length = int(length.decode())

    packet = b""
    while len(packet) != length:
        packet += skt.recv(min(config.get_recv_buffer_size(), length - len(packet)))

    packet = PacketInfo(packet)

    return packet


def gen_len_prefix(length: int) -> bytes:
    """
    Generates a prefix string for the length of the packet.
    :param length: length of the packet
    :return: a prefix string of constant length that represents the length of the packet
    """
    return str(length).zfill(LFS).encode(CHARSET)


def send_packet(skt: socket.socket, packet: bytes) -> None:
    """
    Sends a packet according transmission protocol.
    :param skt: the socket interface that we use to communicate
    :param packet: the packet to send
    """
    prefix = gen_len_prefix(len(packet))
    packet = prefix + packet
    skt.send(packet)
