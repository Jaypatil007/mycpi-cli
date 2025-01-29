import base64
import json
import requests
import click
from .config_manager import ConfigManager
import base64
import json
import requests
import click
from .config_manager import ConfigManager
from .auth import OAuthProvider
from .auth.exceptions import AuthenticationError

class CPIDeployer:
    def __init__(self, env_name):
        self.config = ConfigManager()
        self.config.load_config()
        self.env_config = self.config.config["environments"].get(env_name)
        self.base_url = self.env_config["api_url"]
        self.token_base_url = "https://690b665dtrial.authentication.us10.hana.ondemand.com"
        
        # Initialize auth provider
        self.auth_provider = OAuthProvider(
            token_url=f"{self.token_base_url}/oauth/token",
            client_id=self.env_config["client_id"],
            client_secret=self.env_config["client_secret"]
        )
    
    def _get_auth_token(self):
        try:
            return self.auth_provider.get_token()
        except AuthenticationError as e:
            click.echo(f"🔑 Authentication failed: {str(e)}")
            raise

    

    def deploy_package(self, package_path):
        try:
            # Get token using auth provider
            token = self.auth_provider.get_token()

            csrf_url = f"{self.base_url}/api/v1/"
            csrf_headers = {
                "Authorization": f"Bearer {token}",  # Use token from auth provider
                "Accept": "application/json",
                "X-CSRF-Token": "Fetch"
            }
            csrf_response = requests.head(csrf_url, headers=csrf_headers)

            # click.echo("🔍 CSRF Response Headers:")
            # click.echo(csrf_response.headers)
            # click.echo("🔍 CSRF Response Body:")
            # click.echo(csrf_response.text)

            if csrf_response.status_code != 200:
                click.echo(f"❌ Failed to fetch CSRF token: {csrf_response.text} and {csrf_response.status_code}")
                
            csrf_token = csrf_response.headers.get("x-csrf-token")
            if not csrf_token:
                click.echo("❌ 'csrf_token' header not found in response.")
                return False

            click.echo(f"🔑 CSRF token {csrf_token}.")

            deploy_url = f"{self.base_url}/api/v1/IntegrationPackages?Overwrite=true"
            headers = {
                "Authorization": f"Bearer {token}",  # Use token from auth provider
                "X-CSRF-Token": csrf_token,
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
            
            with open(package_path, 'rb') as pkg:
                zip_content = pkg.read()
                base64_encoded_content = base64.b64encode(zip_content).decode('utf-8')
                payload = {"PackageContent": base64_encoded_content}
                response = requests.post(
                    deploy_url,
                    headers=headers,
                    data=json.dumps(payload)
                )
                
            click.echo("🔍 deployment Response Headers:")
            click.echo(response.headers)
            click.echo(f"🔍 deployment Response Body:   and status code: {response.status_code}")
            click.echo(response.text)

            if response.status_code == 201:
                click.echo("🚀 Deployment initiated successfully!")
                return True
            else:
                click.echo(f"❌ Deployment failed: {response.text}")
                return False
                
        except Exception as e:
            click.echo(f"❌ Deployment error: {str(e)}")
            return False