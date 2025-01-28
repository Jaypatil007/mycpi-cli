import click
from cpi_cli.config_manager import ConfigManager
from cpi_cli.packager import PackageManager
from cpi_cli.deployer import CPIDeployer

@click.group()
def cli():
    """SAP CPI Deployment CLI"""
    pass

@cli.command()
@click.option('--env', required=True, help='Environment name (dev/test/prod)')
@click.option('--api-url', required=True, help='CPI OData API URL')
@click.option('--client-id', required=True, help='OAuth Client ID')
@click.option('--client-secret', required=True, help='OAuth Client Secret')
def configure(env, api_url, client_id, client_secret):
    """Configure environment credentials"""
    cm = ConfigManager()
    cm.configure_environment(env, api_url, client_id, client_secret)

@cli.command()
@click.option('--source', '-s', required=True, help='Source directory')
@click.option('--output', '-o', default='cpi_package.zip', help='Output ZIP file')
def package(source, output):
    """Package CPI project"""
    pm = PackageManager()
    pm.package_project(source, output)

@cli.command()
@click.option('--env', '-e', required=True, help='Target environment')
@click.option('--package', '-p', required=True, help='Package file to deploy')
def deploy(env, package):
    """Deploy package to CPI environment"""
    deployer = CPIDeployer(env)
    if deployer.deploy_package(package):
        click.echo("✅ Deployment successful!")
    else:
        click.echo("❌ Deployment failed")

if __name__ == '__main__':
    cli()