"""

    Accessor for private keys in the environment

"""
import os
import json


class KeyManager(object):
    APP_DEBUG = "APP_DEBUG"
    APP_SECRET = "APP_SECRET"
    DB_NAME = "DB_NAME"
    DB_SCHEMA = "DB_SCHEMA"
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    DB_USER = "DB_USER"
    DB_PASSWORD = "DB_PASSWORD"
    RECAPTCHA_SECRET = "RECAPTCHA_SECRET"
    MANDRILL_API_KEY = "MANDRILL_API_KEY"
    MANDRILL_HOST = "MANDRILL_HOST"
    MANDRILL_PORT = "MANDRILL_PORT"
    MANDRILL_SMTP_USERNAME = "MANDRILL_SMTP_USERNAME"
    MANDRILL_SMTP_PASSWORD = "MANDRILL_SMTP_PASSWORD"
    ADMIN_EMAIL = "ADMIN_EMAIL"

    def __init__(self, key_file_path: str, environment_keys: list, file_keys: list, optional_keys: dict):
        self.all_keys = dict()

        # Validate key names
        for key in environment_keys:
            if not self.is_potential_key(key):
                raise ValueError('Invalid environment key name "{}"'.format(key))
        for key in file_keys:
            if not self.is_potential_key(key):
                raise ValueError('Invalid file key name "{}"'.format(key))

        all_key_names = []
        all_key_names.extend(environment_keys)
        all_key_names.extend(file_keys)

        for key in optional_keys.keys():
            if key not in all_key_names:
                raise ValueError('Invalid optional key name "{}"'.format(key))

        # Initialize optional keys
        for key, value in optional_keys.items():
            self.all_keys[key] = str(value)

        # Load keys from environment variables
        for key in environment_keys:
            value = os.getenv(key)
            if value is None and self.all_keys[key] is None:
                raise ValueError('Missing environment key "{}"'.format(key))
            self.all_keys[key] = str(value)

        # Load keys from file
        with open(key_file_path) as file:
            secret_keys = json.load(file)
            for key in file_keys:
                if key in secret_keys:
                    self.all_keys[key] = str(secret_keys[key])
                elif key not in self.all_keys:
                    raise ValueError('Missing secret key "{}"'.format(key))

        # Make sure each key exists
        for key in all_key_names:
            if key not in self.all_keys.keys():
                raise ValueError('Missing key "{}"'.format(key))

    def get_key(self, key: str) -> str:
        self.validate_key(key)
        return self.all_keys[key]

    def set_key(self, key: str, value: str):
        self.validate_key(key)
        self.all_keys[key] = value

    def is_potential_key(self, key_name: str) -> bool:
        return hasattr(self, key_name)

    def is_key(self, key_name: str) -> bool:
        return key_name in self.all_keys.keys()

    def validate_key(self, key_name: str):
        if self.is_key(key_name):
            return
        if self.is_potential_key(key_name):
            raise ValueError('Key "{}" not implemented'.format(key_name))
        raise ValueError('Invalid key "{}"'.format(key_name))

