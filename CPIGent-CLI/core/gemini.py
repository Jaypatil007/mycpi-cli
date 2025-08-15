import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_gemini_response(prompt: str) -> str:
    """Gets a response from the Gemini API."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")

        if not api_key or api_key == "YOUR_API_KEY_HERE":
            return "[bold red]Error: Gemini API key not found. Please run `!config set api_key <YOUR_KEY>` inside the chat.[/bold red]"

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"[bold red]An error occurred: {e}[/bold red]"
