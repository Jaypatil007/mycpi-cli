# CPIGent CLI

CPIGent CLI is a powerful, interactive command-line interface for communicating with Google's Gemini large language models.

Built with Python, Typer, and Rich, it provides a beautiful and intuitive user experience directly in your terminal, complete with command autocompletion, syntax highlighting, and Markdown rendering.

## Features

- **Interactive Chat:** Engage in a conversation with the Gemini Pro model.
- **Rich Output:** Responses from the AI are beautifully rendered with support for Markdown, including tables, lists, and syntax-highlighted code blocks.
- **Smart Command System:** Use `!` commands to control the CLI without interrupting your conversation (e.g., `!exit`, `!config`).
- **Interactive Command Suggestions:** Start typing `!` to see a numbered list of available commands. Select with arrow keys or a number shortcut.
- **Configuration Management:** Easily set and view your API key and preferred model from the terminal or within the chat.

## Getting Started

### Prerequisites

- Python 3.8+
- A Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/).

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jaypatil007/mycpi-cli.git
    cd mycpi-cli/CPIGent-CLI
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Before you can start a chat, you need to configure your Gemini API key. You can do this in two ways:

1.  **Recommended (Interactive):** Run the `chat` command and set the key from within the chat.
    ```bash
    python main.py chat
    ```
    Inside the chat, type:
    ```
    You: !config set api_key YOUR_API_KEY_HERE
    ```

2.  **Alternative (Terminal):** Set the key directly from your terminal.
    ```bash
    python main.py config set api_key YOUR_API_KEY_HERE
    ```

You can also change the model you are using (the default is `gemini-1.5-pro-latest`).
```bash
python main.py config set model gemini-pro
```

## Usage

### Starting a Chat Session

To begin your conversation with the AI, run:

```bash
python main.py chat
```

This will launch the interactive prompt. Simply type your question and press Enter.

### In-Chat Commands

In-chat commands give you control over the application without needing to exit. They are always prefixed with `!`.

-   **`!help`**: Displays a list of all available in-chat commands.
-   **`!config show`**: Shows the current model and confirms if the API key is set.
-   **`!config set api_key <KEY>`**: Sets or updates your Gemini API key.
-   **`!config set model <MODEL_NAME>`**: Changes the Gemini model to use.
-   **`!exit`** or **`!quit`**: Ends the chat session.
