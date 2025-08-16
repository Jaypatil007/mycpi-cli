import typer
from cli.cpi_commands.packages import list_packages
from cli.cpi_commands.artifacts import list_artifacts

cpi_app = typer.Typer()
list_commands_app = typer.Typer(help="Commands for listing CPI entities.")

@list_commands_app.command("packages")
def packages():
    list_packages()

@list_commands_app.command("artifacts")
def artifacts():
    list_artifacts()

cpi_app.add_typer(list_commands_app, name="list")
