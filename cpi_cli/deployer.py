import base64
import json
import requests
import click
from .config_manager import ConfigManager

class CPIDeployer:
    def __init__(self, env_name):
        self.config = ConfigManager()
        self.config.load_config()
        self.env_config = self.config.config["environments"].get(env_name)
        self.base_url = self.env_config["api_url"]
        self.token_base_url = "https://690b665dtrial.authentication.us10.hana.ondemand.com"
        self.token = self._get_auth_token()

    def _get_auth_token(self):
        try:
            auth_url = f"{self.token_base_url}/oauth/token"
            response = requests.post(auth_url, data={
                "grant_type": "client_credentials",
                "client_id": self.env_config["client_id"],
                "client_secret": self.env_config["client_secret"]
            })
            response.raise_for_status()
            #click.echo(f"❌ Deployment failed: {response.json()["access_token"]}")
            return response.json()["access_token"]
        except requests.exceptions.RequestException as e:
            click.echo(f"🔑 Authentication failed: {str(e)}")
            raise

    def deploy_package(self, package_path):
        try:

            csrf_url = f"{self.base_url}/api/v1/"
            csrf_headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "X-CSRF-Token": "Fetch"
            }
            csrf_response = requests.head(csrf_url, headers=csrf_headers)


            click.echo("🔍 CSRF Response Headers:")
            click.echo(csrf_response.headers)
            click.echo("🔍 CSRF Response Body:")
            click.echo(csrf_response.text)

            #csrf_response = "B9RGeQA8blPFHHeV6TaSGO"
            if csrf_response.status_code != 200:
                click.echo(f"❌ Failed to fetch CSRF token: {csrf_response.text} nad {csrf_response.status_code}")
                #return False
            csrf_token = csrf_response.headers.get("x-csrf-token")
            if not csrf_token:
                click.echo("❌ 'csrf_token' header not found in response.")
                return False

        

            
            click.echo(f"❌ CSRF token {csrf_token}.")
            if not csrf_token:
                click.echo("❌ CSRF token not found in response headers.")
                #return False
            

            deploy_url = f"{self.base_url}/api/v1/IntegrationPackages?Overwrite=true"
            headers = {
                "Authorization": f"Bearer {self.token}",
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
            click.echo("🔍 deployment Response Body:")
            click.echo(response.text)

            
            
            if response.status_code == 202:
                click.echo("🚀 Deployment initiated successfully!")
                return True
            else:
                click.echo(f"❌ Deployment failed: {response.text}")
                return False
        except Exception as e:
            click.echo(f"❌ Deployment error: {str(e)}")
            return False