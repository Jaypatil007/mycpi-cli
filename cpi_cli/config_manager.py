import json
import click
from cryptography.fernet import Fernet
from pathlib import Path

CPI_CONFIG_PATH = Path.home() / ".cpi_config"
KEY_FILE = Path.home() / ".cpi_key"

class ConfigManager:
    def __init__(self):
        self.config = {}
        self.cipher_suite = self._get_or_create_key()

    def _get_or_create_key(self):
        """Get existing key or create a new one"""
        if KEY_FILE.exists():
            with open(KEY_FILE, "rb") as key_file:
                return Fernet(key_file.read())
        else:
            key = Fernet.generate_key()
            KEY_FILE.touch(mode=0o600)
            with open(KEY_FILE, "wb") as key_file:
                key_file.write(key)
            return Fernet(key)

    def load_config(self):
        try:
            with open(CPI_CONFIG_PATH, "rb") as f:
                encrypted_data = f.read()
                decrypted_data = self.cipher_suite.decrypt(encrypted_data)
                self.config = json.loads(decrypted_data)
        except FileNotFoundError:
            self.config = {"environments": {}}

    def save_config(self):
        encrypted_data = self.cipher_suite.encrypt(
            json.dumps(self.config).encode()
        )
        CPI_CONFIG_PATH.parent.mkdir(exist_ok=True)
        with open(CPI_CONFIG_PATH, "wb") as f:
            f.write(encrypted_data)

    # ADD THE MISSING METHOD HERE
    def configure_environment(self, env_name, api_url, client_id, client_secret):
        """Store environment configuration"""
        self.load_config()
        self.config["environments"][env_name] = {
            "api_url": api_url,
            "client_id": client_id,
            "client_secret": client_secret
        }
        self.save_config()
        click.echo(f"✅ Configured environment '{env_name}' successfully!")