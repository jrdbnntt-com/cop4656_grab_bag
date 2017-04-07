"""
    Accessor for private keys in the environment

    This should be at project root in order to function properly
"""

import os
from jrdbnntt_com import key_manager


class Keys(key_manager.KeyManager):
    pass


key_instance = Keys(
    key_file_path=os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/secret_keys.json'),
    environment_keys=[
        Keys.APP_DEBUG
    ],
    file_keys=[
        Keys.APP_SECRET,
        Keys.DB_HOST,
        Keys.DB_PORT,
        Keys.DB_NAME,
        Keys.DB_SCHEMA,
        Keys.DB_USER,
        Keys.DB_PASSWORD
    ],
    optional_keys={
        Keys.APP_DEBUG: False
    }
)


def get_key(key: str) -> str:
    return key_instance.get_key(key)


def set_key(key: str, value: str):
    key_instance.set_key(key, value)

