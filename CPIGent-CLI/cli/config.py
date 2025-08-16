import typer
from rich.console import Console
from rich.panel import Panel
import os
from dotenv import set_key

config_app = typer.Typer()
console = Console()

@config_app.command("set")
def config_set(key: str = typer.Argument(..., help="Config key to set ('api_key' or 'model')."),
               value: str = typer.Argument(..., help="Value to set for the key.")):
    """Sets a configuration value in the .env file."""
    key_upper = key.upper()
    if key_upper not in ["API_KEY", "MODEL"]:
        console.print(f"[bold red]Error: Only 'api_key' and 'model' are supported config keys.[/bold red]")
        raise typer.Exit()

    env_key = f"GEMINI_{key_upper}"
    dotenv_path = ".env"
    set_key(dotenv_path, env_key, value)
    console.print(f"[bold green]Updated {key} to '{value}' in {dotenv_path}[/bold green]")

@config_app.command("show")
def config_show():
    """Shows the current configuration."""
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")

    console.print(Panel(f"[bold]Current Configuration[/bold]\n"
                        f"Model: [cyan]{model_name}[/cyan]", title="CPIGent CLI Config"))

    if api_key and api_key != "YOUR_API_KEY_HERE":
        console.print("[bold green]GEMINI_API_KEY is set.[/bold green]")
    else:
        console.print("[bold red]GEMINI_API_KEY is not set.[/bold red]")
