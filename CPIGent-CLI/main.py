import typer
from cli.chat import start_chat
from cli.config import config_app

app = typer.Typer()

# Add the config command group to the main app
app.add_typer(config_app, name="config")

@app.command()
def chat():
    """Starts an interactive chat session with the Gemini LLM."""
    start_chat()

if __name__ == "__main__":
    app()
