#!/usr/bin/env python3
import asyncio
import atexit
import json
import logging
import os
import platform
import re
import sys
import threading
from datetime import datetime
from time import sleep

import pdfkit
from fuzzywuzzy import process
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from rich.align import Align
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.layout import Layout
from rich.live import Live
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

# Import BARRELMAN modules
try:
    from src.exporters.graphviz.dot_exporter import export_dot_graph
    from src.exporters.html_exporter import export_html
    from src.exporters.markdown_exporter import export_markdown
    from src.lexer import BarrelmanLexer
    from src.preview_server import run_preview_server
except ImportError:
    # Adjust imports if running from a different directory
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    from src.exporters.graphviz.dot_exporter import export_dot_graph
    from src.exporters.html_exporter import export_html
    from src.exporters.markdown_exporter import export_markdown
    from src.lexer import BarrelmanLexer
    from src.preview_server import run_preview_server

console = Console()

# Configure logging
logging.basicConfig(
    filename="cli_app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

with open(
    "/Users/deadcoast/_coding_/python/BARRELMAN/src/barrelman.bman", "rt"
) as code_file:
    code = "\n".join(code_file.readlines()[:10])
    syntax = Syntax(code, "python", line_numbers=True)
console.print(syntax)

# Define PREFERENCES_FILE at the top
PREFERENCES_FILE = "preferences.json"

# Then the load_preferences function


def load_preferences():
    """Load user preferences from a JSON file."""
    try:
        # First try to load from the src directory
        preferences_path = os.path.join(
            os.path.dirname(__file__), PREFERENCES_FILE)

        if os.path.exists(preferences_path):
            with open(preferences_path, "r") as f:
                return json.load(f)
        # Then try the current directory
        elif os.path.exists(PREFERENCES_FILE):
            with open(PREFERENCES_FILE, "r") as f:
                return json.load(f)
    except json.JSONDecodeError:
        logging.error(
            "Failed to decode preferences.json. Using default preferences.")

    # Return default preferences
    return {
        "theme": "default",
        "recent_files": [],
        "default_paths": {"bman_files": "./", "export_directory": "./exports"},
        "export_defaults": {
            "html": {"enabled": True, "dark_mode": False},
            "markdown": {"enabled": False},
            "dot": {"enabled": False},
        },
        "preview_server": {"port": 5000, "auto_reload": True},
        "ui_settings": {
            "show_line_numbers": True,
            "auto_highlight": True,
            "confirm_exit": True,
        },
    }


# Now load preferences
preferences = load_preferences()
current_theme = preferences.get("theme", "default")

# Initialize Rich console
console = Console()

# Initialize PromptSession for arrow key navigation
session = PromptSession()
bindings = KeyBindings()

# Lock for thread-safe console updates
console_lock = threading.Lock()

# Menu options
menu_options = [
    {"key": "1", "name": "System Info", "action": "display_system_info"},
    {"key": "2", "name": "Placeholder", "action": "placeholder"},
    {
        "key": "3",
        "name": "View Code Snippet",
        "action": "display_code_snippet",
    },
    {"key": "4", "name": "Settings", "action": "settings_menu"},
    {"key": "5", "name": "Help", "action": "display_help_menu"},
    {"key": "0", "name": "Exit", "action": "exit_application"},
    *[
        {
            "key": "6",
            "name": "Process BARRELMAN File",
            "action": "process_barrelman_file",
        },
        {
            "key": "7",
            "name": "Start BARRELMAN Preview Server",
            "action": "start_preview_server",
        },
    ],
]


class NullHighlighter(RegexHighlighter):
    base_style = ""
    highlights = [r""]


def highlight_document(doc, keywords, nskip):
    max_len = max(len(token.split(" ")) for token in keywords)
    tokens = re.sub(
        r" +", " ", doc.replace(",", " ,").replace(".",
                                                   " .").replace("\n", " ")
    ).split(" ")
    if max_len == 1:
        highlighted_text = _highlight_one_gram(tokens, keywords)
    else:
        highlighted_text = _highlight_n_gram(tokens, max_len, keywords, nskip)
    # print(highlighted_text)
    console = Console(highlighter=NullHighlighter())
    console.print(highlighted_text)


def _highlight_one_gram(tokens, keywords):
    return " ".join(
        [
            (
                f"[black on #FFFF00]{token}[/]"
                if token.lower() in keywords
                else f"{token}"
            )
            for token in tokens
        ]
    ).strip()


def _highlight_n_gram(tokens, max_len, keywords, nskip):
    n_gram_tokens = [
        [" ".join(tokens[i: i + max_len][: j + 1]) for j in range(max_len)]
        for i, _ in enumerate(tokens)
    ]
    highlighted_text = []
    skip = False

    for n_grams in n_gram_tokens:
        candidate = False

        if not skip:
            for index, n_gram in enumerate(n_grams):

                if n_gram.lower() in keywords:
                    candidate = (
                        f"[black on #FFFF00]{n_gram}[/]" +
                        n_grams[-1].split(n_gram)[-1]
                    )
                    skip = index + 1

            if not candidate:
                candidate = n_grams[0]

            highlighted_text.append(candidate)

        else:
            skip = skip - nskip
    return " ".join(highlighted_text)


doc = "word1 word2 word3 word4 word5 word6 word7 word8 word9 word10"
keywords = ["word2"]
highlight_document(doc, keywords, nskip=1)
highlight_document(doc, keywords, nskip=2)
keywords = ["word5 word6"]
highlight_document(doc, keywords, nskip=1)
highlight_document(doc, keywords, nskip=2)
keywords = ["word2", "word5 word6"]
highlight_document(doc, keywords, nskip=1)
highlight_document(doc, keywords, nskip=2)

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Initialize Rich console
console = Console()


# Define ASCII characters for single and double lines
SINGLE_LINE = {
    "top_left": "┌",
    "top_right": "┐",
    "bottom_left": "└",
    "bottom_right": "┘",
    "horizontal": "─",
    "vertical": "│",
    "cross": "┼",
}

DOUBLE_LINE = {
    "top_left": "╔",
    "top_right": "╗",
    "bottom_left": "╚",
    "bottom_right": "╝",
    "horizontal": "═",
    "vertical": "║",
    "cross": "╬",
}

# Themes and current theme selection
themes = {
    "default": {
        "border_style": "bold magenta",
        "title_style": "bold cyan",
        "option_style": "bold white",
        "highlight_style": "bold yellow",
        "text_style": "white",
    },
    "dark": {
        "border_style": "bold white",
        "title_style": "bold green",
        "option_style": "bold white",
        "highlight_style": "bold red",
        "text_style": "white",
    },
    "light": {
        "border_style": "bold black",
        "title_style": "bold blue",
        "option_style": "bold black",
        "highlight_style": "bold blue",
        "text_style": "black",
    },
}


# =============================================================================
#                        UI/UX FUNCTIONS
# =============================================================================


def save_preferences(preferences):
    """Save user preferences to a JSON file."""
    try:
        # Try to save to the src directory first
        preferences_path = os.path.join(
            os.path.dirname(__file__), PREFERENCES_FILE)

        with open(preferences_path, "w") as f:
            json.dump(preferences, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save preferences to src directory: {e}")
        try:
            # Fall back to current directory
            with open(PREFERENCES_FILE, "w") as f:
                json.dump(preferences, f, indent=4)
        except Exception as e:
            logging.error(f"Failed to save preferences: {e}")


def update_preference(category, setting, value):
    """Update a specific preference setting."""
    preferences = load_preferences()

    # Handle nested preferences
    if "." in category:
        parts = category.split(".")
        current = preferences

        # Navigate to the nested category
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set the value
        current[parts[-1]] = value
    else:
        # Handle direct category
        if category not in preferences:
            preferences[category] = {}

        if isinstance(preferences[category], dict):
            preferences[category][setting] = value
        else:
            # Category is a value, not a dict
            preferences[category] = value

    save_preferences(preferences)
    return preferences


def add_recent_file(file_path):
    """Add a file to the recent files list."""
    preferences = load_preferences()

    # Initialize recent_files if it doesn't exist
    if "recent_files" not in preferences:
        preferences["recent_files"] = []

    # Remove the file if it exists (to prevent duplicates)
    if file_path in preferences["recent_files"]:
        preferences["recent_files"].remove(file_path)

    # Add the file to the beginning of the list
    preferences["recent_files"].insert(0, file_path)

    # Keep only the 10 most recent files
    preferences["recent_files"] = preferences["recent_files"][:10]

    save_preferences(preferences)


def settings_menu():
    while True:
        console.clear()
        console.print("[bold magenta]Settings[/bold magenta]")

        # Load current preferences
        preferences = load_preferences()

        # Create a table to display current preferences
        settings_table = Table(
            title="Current Settings", style=themes[current_theme]["border_style"]
        )
        settings_table.add_column(
            "Setting", style=themes[current_theme]["title_style"])
        settings_table.add_column(
            "Value", style=themes[current_theme]["option_style"])

        # Add theme setting
        settings_table.add_row(
            "Theme", preferences.get("theme", "default").capitalize()
        )

        # Add export defaults
        export_defaults = preferences.get("export_defaults", {})
        html_enabled = (
            "Yes" if export_defaults.get("html", {}).get(
                "enabled", False) else "No"
        )
        html_dark = (
            "Yes" if export_defaults.get("html", {}).get(
                "dark_mode", False) else "No"
        )
        md_enabled = (
            "Yes" if export_defaults.get("markdown", {}).get(
                "enabled", False) else "No"
        )
        dot_enabled = (
            "Yes" if export_defaults.get("dot", {}).get(
                "enabled", False) else "No"
        )

        settings_table.add_row("HTML Export Enabled", html_enabled)
        settings_table.add_row("HTML Dark Mode", html_dark)
        settings_table.add_row("Markdown Export Enabled", md_enabled)
        settings_table.add_row("GraphViz DOT Export Enabled", dot_enabled)

        # Add UI settings
        ui_settings = preferences.get("ui_settings", {})
        line_numbers = "Yes" if ui_settings.get(
            "show_line_numbers", True) else "No"
        auto_highlight = "Yes" if ui_settings.get(
            "auto_highlight", True) else "No"
        confirm_exit = "Yes" if ui_settings.get("confirm_exit", True) else "No"

        settings_table.add_row("Show Line Numbers", line_numbers)
        settings_table.add_row("Auto Syntax Highlight", auto_highlight)
        settings_table.add_row("Confirm on Exit", confirm_exit)

        console.print(settings_table)

        # Menu options
        console.print("\n[bold cyan]Settings Menu:[/bold cyan]")
        console.print("1. Change Theme")
        console.print("2. Export Defaults")
        console.print("3. UI Settings")
        console.print("4. View Recent Files")
        console.print("5. Reset to Default Settings")
        console.print("0. Return to Main Menu")

        choice = Prompt.ask(
            "Enter your choice", choices=["1", "2", "3", "4", "5", "0"], default="0"
        )

        if choice == "1":
            select_theme()
        elif choice == "2":
            export_settings_menu()
        elif choice == "3":
            ui_settings_menu()
        elif choice == "4":
            view_recent_files()
        elif choice == "5":
            reset_preferences()
        elif choice == "0":
            break


def export_settings_menu():
    """Configure export default settings."""
    console.clear()
    console.print("[bold magenta]Export Settings[/bold magenta]")

    preferences = load_preferences()
    export_defaults = preferences.get("export_defaults", {})

    # HTML Export
    html_enabled = (
        Prompt.ask(
            "Enable HTML export by default? (y/n)",
            choices=["y", "n"],
            default=(
                "y" if export_defaults.get("html", {}).get(
                    "enabled", True) else "n"
            ),
        )
        == "y"
    )

    html_dark = False
    if html_enabled:
        html_dark = (
            Prompt.ask(
                "Use dark mode for HTML by default? (y/n)",
                choices=["y", "n"],
                default=(
                    "y"
                    if export_defaults.get("html", {}).get("dark_mode", False)
                    else "n"
                ),
            )
            == "y"
        )

    # Markdown Export
    md_enabled = (
        Prompt.ask(
            "Enable Markdown export by default? (y/n)",
            choices=["y", "n"],
            default=(
                "y"
                if export_defaults.get("markdown", {}).get("enabled", False)
                else "n"
            ),
        )
        == "y"
    )

    # GraphViz DOT Export
    dot_enabled = (
        Prompt.ask(
            "Enable GraphViz DOT export by default? (y/n)",
            choices=["y", "n"],
            default=(
                "y" if export_defaults.get("dot", {}).get(
                    "enabled", False) else "n"
            ),
        )
        == "y"
    )

    # Save settings
    update_preference("export_defaults.html", "enabled", html_enabled)
    update_preference("export_defaults.html", "dark_mode", html_dark)
    update_preference("export_defaults.markdown", "enabled", md_enabled)
    update_preference("export_defaults.dot", "enabled", dot_enabled)

    console.print("[bold green]Export settings updated![/bold green]")
    Prompt.ask("Press Enter to return to the Settings menu")


def ui_settings_menu():
    """Configure UI settings."""
    console.clear()
    console.print("[bold magenta]UI Settings[/bold magenta]")

    preferences = load_preferences()
    ui_settings = preferences.get("ui_settings", {})

    # Line numbers
    line_numbers = (
        Prompt.ask(
            "Show line numbers by default? (y/n)",
            choices=["y", "n"],
            default="y" if ui_settings.get("show_line_numbers", True) else "n",
        )
        == "y"
    )

    # Auto highlight
    auto_highlight = (
        Prompt.ask(
            "Auto syntax highlight by default? (y/n)",
            choices=["y", "n"],
            default="y" if ui_settings.get("auto_highlight", True) else "n",
        )
        == "y"
    )

    # Confirm exit
    confirm_exit = (
        Prompt.ask(
            "Confirm before exiting? (y/n)",
            choices=["y", "n"],
            default="y" if ui_settings.get("confirm_exit", True) else "n",
        )
        == "y"
    )

    # Save settings
    update_preference("ui_settings", "show_line_numbers", line_numbers)
    update_preference("ui_settings", "auto_highlight", auto_highlight)
    update_preference("ui_settings", "confirm_exit", confirm_exit)

    console.print("[bold green]UI settings updated![/bold green]")
    Prompt.ask("Press Enter to return to the Settings menu")


def view_recent_files():
    """View and manage recent files."""
    console.clear()
    console.print("[bold magenta]Recent Files[/bold magenta]")

    preferences = load_preferences()
    recent_files = preferences.get("recent_files", [])

    if not recent_files:
        console.print("[bold yellow]No recent files found.[/bold yellow]")
        Prompt.ask("Press Enter to return to the Settings menu")
        return

    # Display recent files
    table = Table(title="Recent Files",
                  style=themes[current_theme]["border_style"])
    table.add_column("#", style="dim", width=4)
    table.add_column("File Path", style=themes[current_theme]["option_style"])

    for idx, file_path in enumerate(recent_files, 1):
        table.add_row(str(idx), file_path)

    _file_options(
        table,
        "\n[bold cyan]Options:[/bold cyan]",
        "1. Open a file",
        "2. Clear recent files",
    )
    console.print("0. Return to Settings menu")

    choice = Prompt.ask("Enter your choice", choices=[
                        "1", "2", "0"], default="0")

    if choice == "1":
        # Open a file
        file_idx = Prompt.ask(
            "Enter file number to open",
            choices=[str(i) for i in range(1, len(recent_files) + 1)],
        )
        file_path = recent_files[int(file_idx) - 1]

        if not os.path.exists(file_path):
            _return_to_files("[bold red]File not found: ",
                             file_path, view_recent_files)
            return

        # Process the file
        try:
            with open(file_path, "r") as f:
                content = f.read()

            console.print(f"[bold green]Opened: {file_path}[/bold green]")

            _file_options(
                "\n[bold cyan]What would you like to do with this file?[/bold cyan]",
                "1. Process file (highlighting, export)",
                "2. Start preview server",
                "0. Return to Recent Files",
            )
            file_choice = Prompt.ask(
                "Enter your choice", choices=["1", "2", "0"], default="0"
            )

            if file_choice == "1":
                _lexer_processing(content, file_path,
                                  preferences, view_recent_files)
            elif file_choice == "2":
                _extracted_from_view_recent_files_78(
                    content, view_recent_files)
        except Exception as e:
            _return_to_files(
                "[bold red]Error processing file: ", e, view_recent_files)
    elif choice == "2":
        # Clear recent files
        confirm = Prompt.ask(
            "Are you sure you want to clear all recent files? (y/n)",
            choices=["y", "n"],
            default="n",
        )

        if confirm == "y":
            update_preference("recent_files", [], None)  # Clear the list
            console.print("[bold green]Recent files cleared.[/bold green]")

        Prompt.ask("Press Enter to return to the Settings menu")

    elif choice == "0":
        return


def _lexer_processing(content, file_path, preferences, view_recent_files):
    # Process the file with lexer
    lexer = BarrelmanLexer(content)
    # Only tokenize if we're using the tokens or add the file to recent files
    add_recent_file(file_path)

    # Show syntax highlighting by default if enabled in preferences
    if preferences.get("ui_settings", {}).get("auto_highlight", True):
        console.print("[bold cyan]Syntax highlighting:[/bold cyan]")
        lexer.highlight()

        # Ask if the user wants to export in any format
    if (
        Prompt.ask(
            "Would you like to export this file? (y/n)", choices=["y", "n"], default="n"
        )
        == "y"
    ):
        _tokenize_export(lexer, preferences)
    Prompt.ask("Press Enter to return to Recent Files")
    view_recent_files()


def _tokenize_export(lexer, preferences):
    # Now we need to tokenize for export
    tokens = lexer.tokenize()

    # Get export preferences
    export_defaults = preferences.get("export_defaults", {})

    # Offer export options
    console.print("[bold magenta]Export Options:[/bold magenta]")

    if (
        Prompt.ask(
            "Export as HTML? (y/n)",
            choices=["y", "n"],
            default=(
                "y" if export_defaults.get("html", {}).get(
                    "enabled", True) else "n"
            ),
        )
        == "y"
    ):
        dark_mode = (
            Prompt.ask(
                "Use dark mode? (y/n)",
                choices=["y", "n"],
                default=(
                    "y"
                    if export_defaults.get("html", {}).get("dark_mode", False)
                    else "n"
                ),
            )
            == "y"
        )
        export_html(tokens, options={"dark_mode": dark_mode})
        console.print("[bold green]HTML export completed.[/bold green]")

    if (
        Prompt.ask(
            "Export as Markdown? (y/n)",
            choices=["y", "n"],
            default=(
                "y"
                if export_defaults.get("markdown", {}).get("enabled", False)
                else "n"
            ),
        )
        == "y"
    ):
        export_markdown(tokens)
        console.print("[bold green]Markdown export completed.[/bold green]")

    if (
        Prompt.ask(
            "Export as GraphViz DOT? (y/n)",
            choices=["y", "n"],
            default=(
                "y" if export_defaults.get("dot", {}).get(
                    "enabled", False) else "n"
            ),
        )
        == "y"
    ):
        export_dot_graph(tokens)
        console.print(
            "[bold green]GraphViz DOT export completed.[/bold green]")


# TODO Rename this here and in `view_recent_files`
def _extracted_from_view_recent_files_78(content, view_recent_files):
    # Start preview server
    console.print("[bold yellow]Starting preview server...[/bold yellow]")
    console.print(
        "[bold cyan]Open http://127.0.0.1:5000 in your browser to view the preview.[/bold cyan]"
    )

    # Start server in a thread
    preview_thread = threading.Thread(
        target=lambda: run_preview_server(content), daemon=True
    )
    preview_thread.start()

    Prompt.ask("Press Enter to stop the server and return to Recent Files")
    view_recent_files()


def _return_to_files(arg0, arg1, view_recent_files):
    console.print(f"{arg0}{arg1}[/bold red]")
    Prompt.ask("Press Enter to return to Recent Files")
    view_recent_files()


# TODO Rename this here and in `view_recent_files`
def _file_options(arg0, arg1, arg2, arg3):
    # Let user choose what to do with the file
    console.print(arg0)
    console.print(arg1)
    console.print(arg2)
    console.print(arg3)


def reset_preferences():
    """Reset all preferences to default values."""
    console.clear()
    console.print("[bold magenta]Reset Preferences[/bold magenta]")

    confirm = Prompt.ask(
        "Are you sure you want to reset all preferences to default values? (y/n)",
        choices=["y", "n"],
        default="n",
    )

    if confirm == "y":
        # Create default preferences
        default_prefs = {
            "theme": "default",
            "recent_files": [],
            "default_paths": {"bman_files": "./", "export_directory": "./exports"},
            "export_defaults": {
                "html": {"enabled": True, "dark_mode": False},
                "markdown": {"enabled": False},
                "dot": {"enabled": False},
            },
            "preview_server": {"port": 5000, "auto_reload": True},
            "ui_settings": {
                "show_line_numbers": True,
                "auto_highlight": True,
                "confirm_exit": True,
            },
        }

        save_preferences(default_prefs)
        console.print(
            "[bold green]Preferences reset to default values.[/bold green]")

    Prompt.ask("Press Enter to return to the Settings menu")


# =============================================================================
#                DISPLAY FUNCTIONS for BARRELMAN Features
# =============================================================================


def display_weather_menu():
    console.clear()
    city = Prompt.ask("Enter city name")
    fetch_weather(city)
    Prompt.ask("Press Enter to return to the main menu")
    return city


def display_current_time():
    console.clear()
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    console.print(
        f"[bold yellow]Current Date and Time:[/bold yellow] {formatted_time}")
    Prompt.ask("Press Enter to return to the main menu")


def display_real_time_clock():
    console.clear()
    console.print("[bold magenta]Real-Time Clock[/bold magenta]")
    stop_event = threading.Event()

    def update_clock():
        while not stop_event.is_set():
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with console_lock:
                console.print(
                    Align.center(
                        f"Current Time: [bold yellow]{now}[/bold yellow]"),
                    end="\r",
                )
            sleep(1)

    clock_thread = threading.Thread(target=update_clock, daemon=True)
    clock_thread.start()

    try:
        Prompt.ask("Press Enter to return to the main menu")
    finally:
        stop_event.set()


def display_header():
    """
    Clear the console and display the BARRELMAN logo, system information,
    and current date/time before showing the menu.
    """
    console.clear()
    display_logo()  # Provided logo
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sys_info = f"[bold cyan]System:[/bold cyan] {platform.system()} | [bold cyan]Node:[/bold cyan] {platform.node()} | [bold cyan]Time:[/bold cyan] {now}"
    console.print(Align.center(sys_info))
    display_greeting()
    sleep(1)


def display_system_info():
    console.clear()
    console.print("[bold magenta]System Information[/bold magenta]")
    try:
        uname = os.uname()
        info = f"""
        System: {uname.sysname}
        Node Name: {uname.nodename}
        Release: {uname.release}
        Version: {uname.version}
        Machine: {uname.machine}
        """
    except AttributeError:
        # For Windows systems where os.uname() is not available
        info = f"""
        System: {os.name}
        Platform: {sys.platform}
        Python Version: {sys.version}
        """
    table = Table(title="System Info",
                  style=themes[current_theme]["border_style"])
    table.add_column("Attribute", style=themes[current_theme]["title_style"])
    table.add_column("Value", style=themes[current_theme]["text_style"])

    for line in info.strip().split("\n"):
        if ":" in line:
            attr, value = line.split(":", 1)
            table.add_row(attr.strip(), value.strip())

    console.print(table)
    Prompt.ask("Press Enter to return to the main menu")


def display_code_snippet():
    console.clear()
    code = r"""
def greet(name):
    print(f"Hello, {name}!")

greet("World")
"""
    syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
    console.print(syntax)
    Prompt.ask("Press Enter to return to the main menu")


# =============================================================================
#                    BARRELMAN CLI PROMPTING FUNCTIONS
# =============================================================================


@bindings.add("c-s")  # Ctrl+S for searching
def _(event):
    fuzzy_search_menu()


@bindings.add("c-h")  # Ctrl+H for help
def _(event):
    display_help_menu()


@bindings.add("up")
def move_up(event):
    global current_selection
    current_selection = (current_selection - 1) % len(menu_options)
    display_menu()


@bindings.add("down")
def move_down(event):
    global current_selection
    current_selection = (current_selection + 1) % len(menu_options)
    display_menu()


@bindings.add("c-c")  # Ctrl+C to exit
def _(event):
    event.app.exit()


@bindings.add("c-t")  # Ctrl+T to change theme
def _(event):
    select_theme()


def display_preferences():
    console.clear()
    console.print("[bold magenta]User Preferences[/bold magenta]")
    preferences = load_preferences()
    theme = preferences.get("theme", "default")
    console.print(
        f"Current Theme: [bold yellow]{theme.capitalize()}[/bold yellow]")
    Prompt.ask("Press Enter to return to the Settings menu")


def display_help_menu():
    console.clear()
    help_text = """
[bold magenta]BARRELMAN - Help Menu[/bold magenta]

BARRELMAN is a custom domain-specific language (DSL) parser and toolkit that can tokenize,
process, and visualize `.bman` files.

[bold]1. Process BARRELMAN File[/bold]
Description: Process a .bman file with various options including syntax highlighting,
exporting to HTML, Markdown, or GraphViz DOT format.

[bold]2. Start BARRELMAN Preview Server[/bold]
Description: Launch a web server to preview and interact with a .bman file in real-time.

[bold]3. Run Command-Line Interface[/bold]
Description: Execute BARRELMAN with command-line arguments for more control.

[bold]4. Browse BARRELMAN Files[/bold]
Description: Browse directories to find and select .bman files.

[bold]5. Change Theme[/bold]
Description: Customize the appearance of the CLI interface.

[bold]6. System Information[/bold]
Description: Display system information.

[bold]7. Help[/bold]
Description: Shows this help menu.

[bold]0. Exit[/bold]
Description: Exit the application.

[bold]Supported BARRELMAN Features:[/bold]
- Lexical analysis of .bman files
- Syntax highlighting
- HTML, Markdown, and GraphViz DOT export
- Interactive web preview
"""
    console.print(
        Align.center(
            Text(help_text, style=themes[current_theme]["text_style"]))
    )
    Prompt.ask("Press Enter to return to the main menu")


def display_table():
    console.clear()
    table = Table(title="Sample Data", style="bold blue")

    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="bold cyan")
    table.add_column("Description", style="dim")

    table.add_row("1", "Option One", "Description for option one.")
    table.add_row("2", "Option Two", "Description for option two.")
    table.add_row("3", "Option Three", "Description for option three.")
    table.add_row("4", "Option Four", "Description for option four.")

    console.print(table)
    Prompt.ask("Press Enter to return to the main menu")


def handle_choice_arrow():
    selected = 0
    total = len(menu_options)

    # Render the menu with the current selection
    def render_menu():
        with console_lock:
            console.clear()
            display_main_layout()
            table = Table(show_header=False, show_edge=False, box=None)
            for idx, option in enumerate(menu_options):
                if idx == selected:
                    table.add_row(
                        f"> [{themes[current_theme]['highlight_style']}] {option['name']}[/]",
                        style=themes[current_theme]["highlight_style"],
                    )
                else:
                    table.add_row(
                        f"  {option['name']}",
                        style=themes[current_theme]["option_style"],
                    )
            console.print(Align.center(table))

    # Initial render
    render_menu()

    while True:
        # Simplified key handling that avoids API compatibility issues
        choice = Prompt.ask(
            "Choose an option (up/down/enter/c-c)",
            choices=["up", "down", "enter", "c-c"] +
            [str(i) for i in range(total)],
            show_choices=False,
        )

        if choice == "up":
            selected = (selected - 1) % total
            render_menu()
        elif choice == "down":
            selected = (selected + 1) % total
            render_menu()
        elif choice == "enter" or choice.isdigit():
            if choice.isdigit():
                selected = int(choice) % total
            action = menu_options[selected]["action"]
            logging.info(f"Selected option: {menu_options[selected]['name']}")
            execute_action(action)
            render_menu()
        elif choice == "c-c":
            exit_application()


def execute_action(action):
    action_map = {
        "display_system_info": display_system_info,
        "display_code_snippet": display_code_snippet,
        "settings_menu": settings_menu,
        "display_help_menu": display_help_menu,
        "exit_application": exit_application,
        "display_real_time_clock": display_real_time_clock,
        "process_barrelman_file": process_barrelman_file,
        "start_preview_server": start_preview_server,
        "run_cli_with_args": run_cli_with_args,
    }
    func = action_map.get(action)
    if func:
        func()
    else:
        console.print("[bold red]Action not implemented.[/bold red]")
        logging.warning(f"Attempted to execute undefined action: {action}")
        sleep(2)


# =============================================================================
#                      BARRELMAN CLI SEARCH FUNCTIONS
# =============================================================================


def list_files():
    console.clear()
    directory = Prompt.ask("Enter directory path", default=".")
    if not os.path.isdir(directory):
        console.print("[bold red]Invalid directory path.[/bold red]")
    else:
        files = os.listdir(directory)
        if not files:
            console.print(
                "[bold yellow]No files found in the directory.[/bold yellow]")
        else:
            table = Table(title=f"Files in {directory}", style="bold blue")
            table.add_column("Filename", style="white")
            for file in files:
                table.add_row(file)
            console.print(table)
    Prompt.ask("Press Enter to return to the main menu")


def search_menu():
    query = Prompt.ask("Enter search term")
    results = []
    results.extend(
        option for option in menu_options if query.lower() in option["name"].lower()
    )
    if results:
        table = Table(title="Search Results", style="bold blue")
        table.add_column("Option", style="white")
        for option in results:
            table.add_row(option["name"])
        console.print(table)
    else:
        console.print("[bold yellow]No matching options found.[/bold yellow]")
    Prompt.ask("Press Enter to return to the main menu")


def fuzzy_search_menu():
    query = Prompt.ask("Enter search term")
    results, scores = process.extract(query, menu_options, limit=5)

    if not results:
        console.print("[bold yellow]No matching options found.[/bold yellow]")
    else:
        table = Table(title="Search Results", style="bold blue")
        table.add_column("Option", style="white")
        table.add_column("Score", style="dim")
        for option, score in zip(results, scores):
            table.add_row(option, str(score))
        console.print(table)
    Prompt.ask("Press Enter to return to the main menu")


def searchable_help():
    console.clear()
    console.print("[bold magenta]Search Help Documentation[/bold magenta]")
    query = Prompt.ask("Enter keyword to search in help")

    # Sample help contents
    help_contents = {
        "login": "To log in, select the login option from the main menu and enter your credentials.",
        "theme": "Use Ctrl+T to change the theme of the application.",
        "exit": "Select option 0 or press Ctrl+C to exit the application.",
    }

    results = {
        k: v
        for k, v in help_contents.items()
        if query.lower() in k.lower() or query.lower() in v.lower()
    }

    if not results:
        console.print(
            "[bold yellow]No help topics matched your query.[/bold yellow]")
    else:
        for topic, description in results.items():
            console.print(f"[bold]{topic.capitalize()}[/bold]: {description}")
    Prompt.ask("Press Enter to return to the main menu")


# =============================================================================
#                      BARRELMAN CLI UTILITY FUNCTIONS
# =============================================================================


def select_theme():
    global current_theme
    console.clear()
    console.print("[bold magenta]Select a Theme[/bold magenta]")
    for idx, theme in enumerate(themes.keys(), 1):
        console.print(f"[{idx}] {theme.capitalize()}")
    choices = [str(i) for i in range(1, len(themes) + 1)]
    choice = Prompt.ask("Enter the number of your choice",
                        choices=choices, default="1")
    selected_theme = list(themes.keys())[int(choice) - 1]
    current_theme = selected_theme
    console.print(
        f"Theme changed to [bold {themes[selected_theme]['highlight_style']}]"
        f"{selected_theme.capitalize()}[/bold].",
        style="bold green",
    )
    # Save preference
    preferences = load_preferences()
    preferences["theme"] = selected_theme
    save_preferences(preferences)
    logging.info(f"Theme changed to {selected_theme}")
    sleep(2)


def select_theme_table():
    """
    Display available themes in a Rich Table and allow the user to select one.
    """
    global current_theme, themes
    console.clear()
    table = Table(title="Available Themes", style="bold magenta")
    table.add_column("Index", justify="center", style="bold cyan")
    table.add_column("Theme Name", justify="center", style="bold green")
    table.add_column("Border Style", justify="center", style="bold yellow")
    table.add_column("Title Style", justify="center", style="bold blue")
    table.add_column("Option Style", justify="center", style="bold white")
    table.add_column("Highlight Style", justify="center", style="bold red")

    theme_keys = list(themes.keys())
    for idx, key in enumerate(theme_keys, start=1):
        theme_data = themes[key]
        table.add_row(
            str(idx),
            key.capitalize(),
            theme_data["border_style"],
            theme_data["title_style"],
            theme_data["option_style"],
            theme_data["highlight_style"],
        )
    console.print(table)
    choice = Prompt.ask(
        "Enter the number of the theme you want to select",
        choices=[str(i) for i in range(1, len(theme_keys) + 1)],
    )
    selected_theme = theme_keys[int(choice) - 1]
    current_theme = selected_theme
    console.print(
        f"Theme changed to [bold {themes[selected_theme]['highlight_style']}]{selected_theme.capitalize()}[/bold].",
        style="bold green",
    )
    sleep(2)


def start_async_task():
    with Live(
        Align.center(Text("Starting async task...", style="bold yellow")),
        refresh_per_second=10,
    ) as live_display:
        asyncio.run(async_task(live_display))


async def async_task(live_display=None):
    for i in range(100):
        await asyncio.sleep(0.1)
        progress = f"[bold green]{i + 1}%[/bold green] completed."
        if live_display:
            live_display.update(Align.center(
                Text(progress, style="bold green")))
        else:
            # Fallback if no live display is provided
            console.print(Align.center(
                Text(progress, style="bold green")), end="\r")
    console.print("[bold green]Async task completed![/bold green]")


def export_help_to_pdf():
    help_text = """
<h1>Help - CLI Menu Application</h1>
<p>This application provides an interactive menu with various options...</p>
"""
    try:
        with open("help.html", "w") as f:
            f.write(help_text)
        pdfkit.from_file("help.html", "help.pdf")
        console.print(
            "[bold green]Help exported to help.pdf successfully![/bold green]"
        )
    except Exception as e:
        console.print(
            f"[bold red]Failed to export help to PDF: {e}[/bold red]")
        logging.error(f"Export help to PDF error: {e}")


# =============================================================================
#                      BARRELMAN LEXER CLI FUNCTIONS
# =============================================================================


def select_barrelman_file():
    """Prompt the user to select a BARRELMAN (.bman) file."""
    console.clear()
    console.print("[bold magenta]Select BARRELMAN File[/bold magenta]")

    # Try to find .bman files in the current directory
    bman_files = [f for f in os.listdir(".") if f.endswith(".bman")]

    if bman_files:
        console.print(
            "[bold green]Found .bman files in current directory:[/bold green]"
        )
        for idx, file in enumerate(bman_files, 1):
            console.print(f"[{idx}] {file}")

        choices = [str(i) for i in range(1, len(bman_files) + 1)] + ["c"]
        choice = Prompt.ask(
            "Enter number to select file or 'c' to enter custom path", choices=choices
        )

        if choice == "c":
            file_path = Prompt.ask("Enter the path to a .bman file")
        else:
            file_path = bman_files[int(choice) - 1]
    else:
        console.print(
            "[bold yellow]No .bman files found in current directory.[/bold yellow]"
        )
        file_path = Prompt.ask("Enter the path to a .bman file")

    if not os.path.exists(file_path):
        console.print(f"[bold red]File not found: {file_path}[/bold red]")
        return None

    return file_path


def process_barrelman_file():
    """Process a BARRELMAN file with various export options."""
    file_path = select_barrelman_file()
    if not file_path:
        Prompt.ask("Press Enter to return to the main menu")
        return

    console.clear()
    console.print(f"[bold green]Processing {file_path}[/bold green]")

    # Read the file content
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        Prompt.ask("Press Enter to return to the main menu")
        return

    # Show options for processing
    console.print("[bold magenta]Select processing options:[/bold magenta]")

    highlight = (
        Prompt.ask(
            "Syntax highlight in terminal? (y/n)", choices=["y", "n"], default="y"
        )
        == "y"
    )
    export_html_option = (
        Prompt.ask("Export as HTML? (y/n)",
                   choices=["y", "n"], default="n") == "y"
    )
    dark_mode = False
    if export_html_option:
        dark_mode = (
            Prompt.ask("Use dark mode for HTML? (y/n)",
                       choices=["y", "n"], default="n")
            == "y"
        )
    export_markdown_option = (
        Prompt.ask("Export as Markdown? (y/n)",
                   choices=["y", "n"], default="n") == "y"
    )
    export_dot = (
        Prompt.ask("Export as GraphViz DOT? (y/n)",
                   choices=["y", "n"], default="n")
        == "y"
    )

    # Process the file with selected options
    console.print("[bold cyan]Processing file...[/bold cyan]")

    try:
        # Create lexer and tokenize
        lexer = BarrelmanLexer(content)
        tokens = lexer.tokenize()

        # Apply selected options
        if highlight:
            console.print("[bold cyan]Syntax highlighting:[/bold cyan]")
            lexer.highlight()

        if export_html_option:
            export_html(tokens, options={"dark_mode": dark_mode})
            console.print("[bold green]HTML export completed.[/bold green]")

        if export_markdown_option:
            export_markdown(tokens)
            console.print(
                "[bold green]Markdown export completed.[/bold green]")

        if export_dot:
            export_dot_graph(tokens)
            console.print(
                "[bold green]GraphViz DOT export completed.[/bold green]")

        console.print("[bold green]Processing complete![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error processing file: {e}[/bold red]")

    Prompt.ask("Press Enter to return to the main menu")


def start_preview_server():
    """Start the BARRELMAN preview server."""
    file_path = select_barrelman_file()
    if not file_path:
        Prompt.ask("Press Enter to return to the main menu")
        return

    console.clear()
    console.print(
        f"[bold green]Starting preview server for {file_path}[/bold green]")

    # Read the file content
    try:
        with open(file_path, "r") as f:
            content = f.read()
    except Exception as e:
        console.print(f"[bold red]Error reading file: {e}[/bold red]")
        Prompt.ask("Press Enter to return to the main menu")
        return

    console.print(
        "[bold yellow]Starting preview server in a new thread. Press Ctrl+C to stop.[/bold yellow]"
    )
    console.print(
        "[bold cyan]Open http://127.0.0.1:5000 in your browser to view the preview.[/bold cyan]"
    )

    # Run the preview server in a new thread so we don't block the CLI
    preview_thread = threading.Thread(
        target=lambda: run_preview_server(content), daemon=True
    )
    preview_thread.start()

    # Wait for user to press Enter to return to the main menu
    try:
        Prompt.ask("Press Enter to stop the server and return to the main menu")
    except KeyboardInterrupt:
        pass

    console.print("[bold yellow]Stopping preview server...[/bold yellow]")


def confirm_exit():
    confirm = Prompt.ask(
        "Are you sure you want to exit? (y/n)", choices=["y", "n"], default="n"
    )
    return confirm.lower() == "y"


def cleanup():
    # Perform necessary cleanup actions
    console.print("\n[bold red]Cleaning up before exit...[/bold red]")
    # Example: Save preferences, close database connections, etc.
    save_preferences(load_preferences())
    logging.info("Application exited gracefully.")


def exit_application():
    """Exit the application after confirmation."""
    if confirm_exit():
        cleanup()
        sys.exit(0)


# =============================================================================
#                         BARRELMAN CLI Main Menu
# =============================================================================


def run_cli_with_args():
    """
    Runs the original BARRELMAN CLI with command-line arguments.
    This provides the same functionality as the original cli.py.
    """
    console.clear()
    console.print(
        "[bold magenta]BARRELMAN Command-Line Interface[/bold magenta]")
    console.print(
        "[bold yellow]This will run the BARRELMAN CLI with command-line arguments[/bold yellow]"
    )

    # Get input file
    file_path = select_barrelman_file()
    if not file_path:
        Prompt.ask("Press Enter to return to the main menu")
        return

    # Get options
    options = []

    if (
        Prompt.ask("Enable syntax highlighting? (y/n)",
                   choices=["y", "n"], default="n")
        == "y"
    ):
        options.append("--highlight")

    if Prompt.ask("Export as HTML? (y/n)", choices=["y", "n"], default="n") == "y":
        options.append("--html")
        if (
            Prompt.ask("Use dark mode for HTML? (y/n)",
                       choices=["y", "n"], default="n")
            == "y"
        ):
            options.append("--dark-mode")

    if Prompt.ask("Export as Markdown? (y/n)", choices=["y", "n"], default="n") == "y":
        options.append("--markdown")

    if (
        Prompt.ask("Export as GraphViz DOT? (y/n)",
                   choices=["y", "n"], default="n")
        == "y"
    ):
        options.append("--dot")

    if (
        Prompt.ask("Start preview server? (y/n)",
                   choices=["y", "n"], default="n")
        == "y"
    ):
        options.append("--preview")

    # Simulate CLI argument parsing
    console.print(
        "[bold green]Running BARRELMAN CLI with options:[/bold green]")

    command = f"barrelman {file_path} {' '.join(options)}"
    console.print(f"[bold cyan]Command:[/bold cyan] {command}")

    # Execute with the options
    try:
        with open(file_path, "r") as f:
            content = f.read()

        lexer = BarrelmanLexer(content)
        tokens = lexer.tokenize()

        for option in options:
            if option == "--highlight":
                console.print("[bold cyan]Syntax highlighting:[/bold cyan]")
                lexer.highlight()
            elif option == "--html":
                dark_mode = "--dark-mode" in options
                export_html(tokens, options={"dark_mode": dark_mode})
                console.print(
                    "[bold green]HTML export completed.[/bold green]")
            elif option == "--markdown":
                export_markdown(tokens)
                console.print(
                    "[bold green]Markdown export completed.[/bold green]")
            elif option == "--dot":
                export_dot_graph(tokens)
                console.print(
                    "[bold green]GraphViz DOT export completed.[/bold green]")
            elif option == "--preview":
                console.print(
                    "[bold yellow]Starting preview server...[/bold yellow]")
                console.print(
                    "[bold cyan]Open http://127.0.0.1:5000 in your browser to view the preview.[/bold cyan]"
                )
                console.print(
                    "[bold yellow]Press Ctrl+C to stop when done.[/bold yellow]"
                )
                run_preview_server(content)

        console.print(
            "[bold green]BARRELMAN CLI execution completed![/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error executing CLI: {e}[/bold red]")

    Prompt.ask("Press Enter to return to the main menu")


def main():
    """
    BARRELMAN's interactive CLI, providing a user-friendly interface for:

    - Processing BARRELMAN files with syntax highlighting
    - Exporting to various formats (HTML, Markdown, GraphViz DOT)
    - Viewing and editing files with live preview
    - Running the command-line interface with arguments
    """
    while True:
        display_header()
        # Build the main menu as a Rich Table
        menu_table = Table(
            title="BARRELMAN Interface", style=themes[current_theme]["border_style"]
        )
        menu_table.add_column(
            "Option",
            justify="center",
            style=themes[current_theme]["title_style"],
            no_wrap=True,
        )
        menu_table.add_column(
            "Description", justify="left", style=themes[current_theme]["option_style"]
        )

        # BARRELMAN-specific options first
        menu_table.add_row("1", "Process BARRELMAN File (highlight, export)")
        menu_table.add_row("2", "Start BARRELMAN Preview Server")
        menu_table.add_row("3", "Run Command-Line Interface")
        menu_table.add_row("4", "Browse BARRELMAN Files")

        # General UI options
        menu_table.add_row("5", "Change Theme")
        menu_table.add_row("6", "System Information")
        menu_table.add_row("7", "Help")
        menu_table.add_row("0", "Exit BARRELMAN")

        console.print(Align.center(menu_table))

        choice = Prompt.ask(
            "Enter your choice",
            choices=["1", "2", "3", "4", "5", "6", "7", "0"],
            default="0",
        )
        logging.info(f"User selected option: {choice}")

        if choice == "1":
            process_barrelman_file()
        elif choice == "2":
            start_preview_server()
        elif choice == "3":
            run_cli_with_args()
        elif choice == "4":
            list_files()
        elif choice == "5":
            select_theme_table()
        elif choice == "6":
            display_system_info()
        elif choice == "7":
            display_help_menu()
        elif choice == "0":
            console.print("[bold red]Exiting BARRELMAN. Goodbye![/bold red]")
            logging.info("User exited BARRELMAN.")
            break
        else:
            console.print(
                "[bold red]Invalid option. Please try again.[/bold red]")
            sleep(2)


if __name__ == "__main__":
    atexit.register(cleanup)  # Register cleanup once
    try:
        main()
    except Exception as e:
        console.print(
            f"[bold red]An unexpected error occurred: {e}[/bold red]")
        logging.exception("An unexpected error occurred.")
        sys.exit(1)

# Add missing function definitions


def display_logo():
    """Displays an ASCII logo."""
    logo = r"""
███████████████████████████████████████████████████████████
█▄─▄─▀██▀▄─██▄─▄▄▀█▄─▄▄▀█▄─▄▄─█▄─▄███▄─▀█▀─▄██▀▄─██▄─▀█▄─▄█
██─▄─▀██─▀─███─▄─▄██─▄─▄██─▄█▀██─██▀██─█▄█─███─▀─███─█▄▀─██
▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀
    """
    styled_logo = Text(logo, style="bold green")
    with console_lock:
        console.print(Align.center(styled_logo))


def display_greeting():
    greeting = "Welcome to the BARRELMAN CLI, Please see options below..."
    with console_lock:
        console.print(
            Align.center(
                Text(greeting, style=themes[current_theme]["text_style"]))
        )


def display_menu():
    """Displays the main menu frame."""
    title = f"[{themes[current_theme]['title_style']}]=== Main Menu ===[/]"
    options = "\n".join(
        [f"[{opt['key']}] {opt['name']}" for opt in menu_options])
    menu_content = f"{title}\n{options}"
    frame = create_frame(menu_content, width=50, ascii_style="double")
    with console_lock:
        console.print(Align.center(frame))


def create_frame(content: str, width: int = 60, ascii_style="double") -> Text:
    """
    Creates a custom frame around the content using specified ASCII style.
    """
    line_chars = SINGLE_LINE if ascii_style == "single" else DOUBLE_LINE
    tl = line_chars["top_left"]
    tr = line_chars["top_right"]
    bl = line_chars["bottom_left"]
    br = line_chars["bottom_right"]
    h = line_chars["horizontal"]
    v = line_chars["vertical"]

    # Build the top border
    top_border = f"{tl}{h * (width - 2)}{tr}"

    # Split content into lines
    content_lines = content.split("\n")

    # Build the middle content with borders
    middle = ""
    for line in content_lines:
        # Pad the line to fit the width
        padded_line = line.ljust(width - 4)
        middle += f"{v}  {padded_line}  {v}\n"

    # Build the bottom border
    bottom_border = f"{bl}{h * (width - 2)}{br}"

    # Combine all parts
    full_frame = f"{top_border}\n{middle}{bottom_border}"

    return Text(full_frame, style=themes[current_theme]["border_style"])


def display_main_layout():
    """Displays the main layout with header, body, and footer."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=12),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=3),
    )

    # Header with logo and greeting
    header_content = (
        Text(
            """
███████████████████████████████████████████████████████████
█▄─▄─▀██▀▄─██▄─▄▄▀█▄─▄▄▀█▄─▄▄─█▄─▄███▄─▀█▀─▄██▀▄─██▄─▀█▄─▄█
██─▄─▀██─▀─███─▄─▄██─▄─▄██─▄█▀██─██▀██─█▄█─███─▀─███─█▄▀─██
▀▄▄▄▄▀▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▄▄▄▄▄▀▄▄▄▀▄▄▄▀▄▄▀▄▄▀▄▄▄▀▀▄▄▀
    """,
            style="bold green",
        )
        + "\n"
        + Text(
            "Welcome to the BARRELMAN Interface!",
            style=themes[current_theme]["text_style"],
        )
    )
    layout["header"].update(Align.center(header_content))

    # Body with menu
    title = f"[{themes[current_theme]['title_style']}]=== Main Menu ===[/]"
    options = "\n".join(
        [f"[{opt['key']}] {opt['name']}" for opt in menu_options])
    menu_content = f"{title}\n{options}"
    frame = create_frame(menu_content, width=50, ascii_style="double")
    layout["body"].update(Align.center(frame))

    # Footer with current time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    footer_text = Text(
        f"Current Time: {now}", style=themes[current_theme]["text_style"]
    )
    layout["footer"].update(Align.center(footer_text))

    console.print(layout)


def fetch_weather(city):
    """Placeholder for weather function - not used in BARRELMAN functionality."""
    console.print(
        "[bold yellow]Weather functionality is not available in this version.[/bold yellow]"
    )
