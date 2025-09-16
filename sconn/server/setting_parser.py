from yaml import dump, load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
    
from sconn.protocol.constants import DEFAULT_SETTINGS


SETTINGS_YAML_PATH = "server_settings.yaml"


def get_setting(setting_name: str) -> str:
    f = open(SETTINGS_YAML_PATH, "r")
    settings_dict = load(f.read(), Loader=Loader)
    f.close()
    return settings_dict[setting_name]


def create_default_settings_yaml() -> None:
    f = open(SETTINGS_YAML_PATH, "w")
    yaml_dict = DEFAULT_SETTINGS
    yaml_dict["certificate_path"] = "server_certificate.pem"
    yaml_dict["certificate_key_path"] = "server_certificate_key.pem"
    yaml_dict["use_mtls"] = False
    f.write(dump(DEFAULT_SETTINGS, Dumper=Dumper))
    f.close()
