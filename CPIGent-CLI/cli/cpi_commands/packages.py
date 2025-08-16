from cli.cpi_commands.auth import get_oauth_token, get_csrf_token, get_cpi_credentials
import requests
import json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

def list_packages():
    """Lists all integration packages from SAP CPI."""
    credentials = get_cpi_credentials()
    if not credentials:
        return

    access_token = get_oauth_token()
    if not access_token:
        return

    csrf_token = get_csrf_token(access_token)
    if not csrf_token:
        return

    base_url = credentials['url']
    url = f"{base_url}/api/v1/IntegrationPackages"

    headers = {
        'X-CSRF-Token': csrf_token,
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    try:
        with console.status("[bold green]Fetching integration packages...[/bold green]"):
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        packages = data.get("d", {}).get("results", [])
        
        if not packages:
            console.print(Panel("[bold yellow]No integration packages found.[/bold yellow]", title="[bold cyan]CPI Integration Packages[/bold cyan]", border_style="cyan"))
            return

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Package ID", style="bold magenta")

        for package in packages:
            package_id = package.get("Id", "N/A")
            table.add_row(package_id)

        console.print(Panel(table, title="[bold cyan]CPI Integration Packages[/bold cyan]", border_style="cyan"))

    except requests.exceptions.RequestException as e:
        console.print(Panel(f"[bold red]Error listing packages: {e}[/bold red]", title="[bold red]Error[/bold red]", border_style="red"))
    except Exception as e:
        console.print(Panel(f"[bold red]An unexpected error occurred: {e}[/bold red]", title="[bold red]Error[/bold red]", border_style="red"))
