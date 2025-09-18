from enum import IntEnum

class ConnectionTypes(IntEnum):
    SERVER_CLIENT   = 1
    CLIENT_CLIENT   = 2
    OPEN_BROADCAST  = 3
    BROADCAST_GROUP = 4
