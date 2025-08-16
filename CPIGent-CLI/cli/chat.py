from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import os
from dotenv import load_dotenv
import shlex
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from core.gemini import get_gemini_response
from cli.config import config_app
from cli.cpi_commands.main import cpi_app

load_dotenv()
console = Console()

class NumberedCompleter(Completer):
    def __init__(self, words):
        self.words = words
        self.current_completions = []

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.lstrip()
        if not text.startswith('!'):
            return

        filtered_words = [word for word in self.words if word.startswith(text)]
        self.current_completions = filtered_words

        for i, word in enumerate(filtered_words, 1):
            if i > 9: break
            yield Completion(
                word,
                start_position=-len(text),
                display=f"{i}. {word}"
            )

def handle_chat_command(command_str: str):
    try:
        parts = shlex.split(command_str)
        command_name = parts[0]
        args = parts[1:]
    except (ValueError, IndexError):
        console.print("[bold red]Invalid command format.[/bold red]")
        return

    if command_name == "config":
        try:
            config_app(args)
        except SystemExit:
            pass
        except Exception as e:
            console.print(f"[bold red]Error executing config command: {e}[/bold red]")
    elif command_name == "cpi":
        try:
            cpi_app(args)
        except SystemExit:
            pass
        except Exception as e:
            console.print(f"[bold red]Error executing CPI command: {e}[/bold red]")
    else:
        console.print(f"[bold red]Unknown command: {command_name}. Try !help.[/bold red]")

def start_chat():
    """Starts an interactive chat session with the Gemini LLM."""
    
    # ASCII Art for the welcome screen
    welcome_art = """
[bold cyan]
      ░██████  ░█████████  ░██████         ░███                                        ░██    
     ░██   ░██ ░██     ░██   ░██          ░██░██                                       ░██    
    ░██        ░██     ░██   ░██         ░██  ░██   ░████████  ░███████  ░████████  ░████████ 
    ░██        ░█████████    ░██        ░█████████ ░██    ░██ ░██    ░██ ░█████████    ░██    
    ░██        ░██           ░██        ░██    ░██ ░██    ░██ ░█████████ ░██    ░██    ░██    
     ░██   ░██ ░██           ░██        ░██    ░██ ░██   ░███ ░██        ░██    ░██    ░██    
      ░██████  ░██         ░██████      ░██    ░██  ░█████░██  ░███████  ░██    ░██     ░████ 
                                                          ░██                                 
                                                    ░███████                                  
                                                                                          
[/bold cyan]
    """
    
    welcome_message = "Welcome to the CPIGent CLI! Type a prompt or `!help` for commands."
    
    console.print(Panel(
        f"{welcome_art}\n[green]{welcome_message}[/green]",
        title="CPIGent CLI",
        border_style="green"
    ))

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        console.print("[bold yellow]Gemini API key not configured. Use `!config set api_key <YOUR_KEY>` to set it.[/bold yellow]")

    commands = ["!help", "!exit", "!quit", "!config set api_key ", "!config set model ", "!config show", "!cpi list packages", "!cpi list artifacts"]
    completer = NumberedCompleter(commands)
    
    style = Style.from_dict({
        'prompt': 'bold cyan',
        'completion-menu.completion': '', 
        'completion-menu.completion.current': 'bold yellow',
        'completion-menu.border': 'black',
        'completion-menu': 'bg:default',
    })

    kb = KeyBindings()
    for i in range(1, 10):
        @kb.add(str(i), eager=True)
        def _(event, num=i):
            b = event.app.current_buffer
            if b.complete_state:
                completions = b.complete_state.completions
                if num <= len(completions):
                    b.apply_completion(completions[num - 1])
    
    session = PromptSession(
        completer=completer, 
        style=style, 
        key_bindings=kb,
        complete_while_typing=True,
        complete_in_thread=True
    )

    while True:
        try:
            prompt = session.prompt([('class:prompt', 'You: ')])

            if not prompt:
                continue

            if prompt.startswith("!"):
                command = prompt[1:].lower().strip()
                if command in ["exit", "quit"]:
                    console.print("[bold yellow]Session ended.[/bold yellow]")
                    break
                elif command == "help":
                     console.print("[bold]Available commands:[/] \n- `!exit` or `!quit`: End the session.\n- `!config set <key> <value>`: Set a config key (api_key, model).\n- `!config show`: Show current configuration.\n- `!cpi list packages`: List SAP CPI integration packages.\n- `!cpi list artifacts`: List SAP CPI integration runtime artifacts.")
                else:
                    handle_chat_command(command)
                continue

            with console.status("[bold green]Generating response...[/bold green]"):
                response_text = get_gemini_response(prompt)

            response_markdown = Markdown(response_text)
            console.print(Panel(response_markdown, title="[bold magenta]Gemini[/bold magenta]", border_style="magenta"))

        except KeyboardInterrupt:
            console.print("\n[bold yellow]Session ended.[/bold yellow]")
            break
        except EOFError:
            console.print("\n[bold yellow]Session ended.[/bold yellow]")
            break
