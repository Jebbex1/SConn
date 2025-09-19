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
server_hostname: 127.0.0.1
"""


def get_setting(setting_name: str, server_side: bool = False) -> str:
    """Given a setting name, retrieve the content of that setting from the appropriate .yaml file.

    :param setting_name: The name of the setting as it is in the yaml config file.
    :type setting_name: str
    :param server_side: A bool indicating if to open the server-side file or not, defaults to False
    :type server_side: bool, optional
    :return: The content of the setting
    :rtype: str
    """
    path = SERVER_CONFIG_PATH if server_side else CLIENT_CONFIG_PATH
    f = open(path, "r")
    settings_dict = load(f.read(), Loader=Loader)
    f.close()
    return settings_dict[setting_name]


def create_default_config(server_side: bool = False) -> None:
    """Creates a default config in the appropriate path.

    :param server_side: is the config relating to the server or not, defaults to False
    :type server_side: bool, optional
    """
    path = SERVER_CONFIG_PATH if server_side else CLIENT_CONFIG_PATH
    content = SERVER_DEFAULT_CONFIG if server_side else CLIENT_DEFAULT_CONFIG
    f = open(path, "w")
    f.write(content)
    f.close()
