import os
from sconn.server.setting_parser import create_default_settings_yaml, get_setting, SETTINGS_YAML_PATH
from sconn.protocol.constants import DEFAULT_SETTINGS


EXPECTED_DEFAULT_SETTINGS = (
    "certificate_key_path: server_certificate_key.pem\n"
    "certificate_path: server_certificate.pem\n"
    "charset: utf-8\n"
    "length_field_header: 32\n"
    "max_field_size: 128\n"
    "max_file_size: 16000000\n"
    "max_title_size: 128\n"
    "port: 8374\n"
    "use_mtls: false\n"
)


def test_default_settings_creation() -> None:
    create_default_settings_yaml()
    created = open(SETTINGS_YAML_PATH, "r").read()
    assert created == EXPECTED_DEFAULT_SETTINGS
    os.remove(SETTINGS_YAML_PATH)


def test_get_setting() -> None:
    create_default_settings_yaml()
    for key, val in DEFAULT_SETTINGS.items():
        assert val == get_setting(key)
    os.remove(SETTINGS_YAML_PATH)
    