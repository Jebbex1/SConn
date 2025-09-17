from yaml import dump, load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


SERVER_CONFIG_PATH = "sconn_server_config_path.yaml"
CLIENT_CONFIG_PATH = "sconn_client_config_path.yaml"

SERVER_DEFAULT_CONFIG = \
    """
    # tls certificates to load as own
    certificate_key_path: server_certificate_key.pem
    certificate_path: server_certificate.pem

    # protocol
    port: 8374
    """

CLIENT_DEFAULT_CONFIG = \
    """
    # trusted CA certificate path
    ca_certificate_path: ca_cert.pem
    
    # protocol
    port: 8374
    """


def get_setting(setting_name: str, server_side: bool = False) -> str:
    path = SERVER_CONFIG_PATH if server_side else CLIENT_CONFIG_PATH
    f = open(path, "r")
    settings_dict = load(f.read(), Loader=Loader)
    f.close()
    return settings_dict[setting_name]


def create_default_config(server_side: bool = False) -> None:
    path = SERVER_CONFIG_PATH if server_side else CLIENT_CONFIG_PATH
    content = SERVER_DEFAULT_CONFIG if server_side else CLIENT_DEFAULT_CONFIG
    f = open(path, "w")
    f.write(content)
    f.close()
