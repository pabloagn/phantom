# phantom_canon/cli_display.py
import time
from contextlib import contextmanager
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.rule import Rule
from rich.table import Table
from rich.text import Text

# --- Global Console ---
# Use force_terminal=True if running in environments where TTY might not be detected correctly (like some CI)
# Adjust width as needed, or let it detect automatically.
console = Console(color_system="auto", force_terminal=True, width=120)

# --- Configuration ---
# Define color styles consistently
STYLE_HEADER = "bold cyan"
STYLE_SUB_HEADER = "bold blue"
STYLE_TASK_SUCCESS = "bold green"
STYLE_TASK_FAILURE = "bold red"
STYLE_TASK_WARNING = "bold yellow"
STYLE_INFO = "dim"
STYLE_EMPHASIS = "italic"
STYLE_FILENAME = "italic magenta"
STYLE_ERROR_TRACE = "red"

# --- Logging Handler ---
def get_rich_logger_handler(level: str = "INFO") -> RichHandler:
    """Creates a configured RichHandler for logging."""
    return RichHandler(
        level=level,
        console=console,
        show_path=False,  # Don't show the full path to the logging module
        show_level=True,
        show_time=True,
        markup=True,  # Allow rich markup in log messages
        rich_tracebacks=True, # Use rich for tracebacks
        tracebacks_show_locals=False, # Don't show local variables in tracebacks by default
        omit_repeated_times=False, # Show timestamp for every log message
    )

# --- Basic Output Functions ---
def print_header(title: str):
    """Prints a main section header rule."""
    console.print(Rule(Text(title, style=STYLE_HEADER), style=STYLE_HEADER), justify="center")

def print_sub_header(title: str, style: str = STYLE_SUB_HEADER):
    """Prints a subsection rule."""
    console.print(Rule(Text(title, style=style), style=style, align="left"))

def print_info(message: str):
    """Prints an informational message with dim styling."""
    console.print(Text(message, style=STYLE_INFO))

def print_emphasis(message: str):
     """Prints a message with emphasis."""
     console.print(Text(message, style=STYLE_EMPHASIS))

def print_filename(path: str):
     """Prints a filename/path with specific styling."""
     console.print(f" -> [{STYLE_FILENAME}]{path}[/]")

# --- Task Status Functions ---
def task_start(message: str):
    """Indicates the start of a task."""
    # Using Spinner might be nice here for longer tasks, or just simple text
    console.print(f":hourglass_flowing_sand: {message}...")

def task_success(message: str, details: Optional[str] = None):
    """Indicates successful completion of a task."""
    full_message = f":heavy_check_mark: [{STYLE_TASK_SUCCESS}]{message}[/]"
    if details:
        full_message += f" ([dim]{details}[/])"
    console.print(full_message)

def task_failure(message: str, details: Optional[str] = None):
    """Indicates failure of a task."""
    full_message = f":x: [{STYLE_TASK_FAILURE}]{message}[/]"
    if details:
        full_message += f" ([dim]{details}[/])"
    console.print(full_message)

def task_warning(message: str, details: Optional[str] = None):
     """Indicates a warning during a task."""
     full_message = f":warning: [{STYLE_TASK_WARNING}]{message}[/]"
     if details:
        full_message += f" ([dim]{details}[/])"
     console.print(full_message)


# --- Summary and Error Display ---
def print_summary(duration: float, success: bool):
    """Prints a final summary panel."""
    status_text = Text("SUCCESS", style=STYLE_TASK_SUCCESS) if success else Text("FAILED", style=STYLE_TASK_FAILURE)
    duration_text = Text(f"{duration:.2f} seconds", style="bold")

    summary_table = Table.grid(padding=(0, 1))
    summary_table.add_column()
    summary_table.add_column()
    summary_table.add_row("Overall Status:", status_text)
    summary_table.add_row("Total Duration:", duration_text)

    console.print(Panel(summary_table, title="Summary", border_style="dim", padding=(1, 2)))

def print_exception(show_locals: bool = False):
    """Prints a nicely formatted exception traceback."""
    console.print_exception(show_locals=show_locals, word_wrap=True)

# --- Progress Bar Context Manager (Optional but Recommended for Loops) ---
@contextmanager
def get_progress_bar(*columns, description: str = "Processing..."):
    """Provides a rich Progress context manager."""
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        *columns, # Add standard columns like Bar, Percentage, Time
        console=console,
        transient=True # Hides progress bar on completion
    )
    try:
        yield progress
    finally:
        progress.stop()

# Standard columns for item processing progress
default_progress_columns = (
    BarColumn(),
    TaskProgressColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
    TimeRemainingColumn(),
)