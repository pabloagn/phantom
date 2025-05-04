# packages/phantom-visuals/phantom_visuals/utils/logging.py

"""Logging configuration for phantom-visuals.

This module sets up logging for the application with support for
console and file output, formatted using rich.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.theme import Theme
from rich.traceback import install as install_rich_traceback

# Install rich traceback handler for better exception formatting
install_rich_traceback(show_locals=True, width=100, word_wrap=True)

# Custom theme for phantom-visuals
PHANTOM_THEME = Theme(
    {
        "info": "bold cyan",
        "warning": "bold yellow",
        "error": "bold red",
        "critical": "bold white on red",
        "debug": "dim cyan",
        "success": "bold green",
        "highlight": "bold magenta",
        "processing": "bold blue",
        "parameter": "cyan",
        "value": "bright_white",
        "header": "bold cyan on dark_blue",
        "subheader": "dim cyan",
        "phantom": "bold magenta",
        "caption": "italic bright_black",
        "filename": "bright_blue underline",
        "time": "bright_black",
        "progress.description": "bright_cyan",
        "progress.percentage": "bright_magenta",
        "progress.remaining": "bright_black",
    }
)

# Global console for rich output with phantom theme
console = Console(theme=PHANTOM_THEME, highlight=True)

# Default log directory
DEFAULT_LOG_DIR = Path("logs")

# Colors and styles
LOG_COLORS = {
    "DEBUG": "debug",
    "INFO": "info",
    "WARNING": "warning",
    "ERROR": "error",
    "CRITICAL": "critical",
}


def setup_logging(
    level: str = "INFO",
    log_dir: Optional[Union[str, Path]] = None,
    log_file: Optional[str] = None,
    capture_warnings: bool = True,
) -> logging.Logger:
    """Configure logging for phantom-visuals.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory to store log files (defaults to "logs")
        log_file: Log filename (defaults to phantom_visuals_YYYYMMDD.log)
        capture_warnings: Whether to capture Python warnings

    Returns:
        Configured logger instance
    """
    # Set up log directory
    if log_dir is None:
        log_dir = DEFAULT_LOG_DIR

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Set up log file
    if log_file is None:
        timestamp = time.strftime("%Y%m%d")
        log_file = f"phantom_visuals_{timestamp}.log"

    log_path = log_dir / log_file

    # Configure root logger
    logging.basicConfig(
        level=level.upper(),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            # Rich console handler with customizations
            RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                show_time=True,
                show_path=False,
                markup=True,
                enable_link_path=True,
                log_time_format="[%X]",
                omit_repeated_times=False,
                keywords=[
                    "ERROR",
                    "WARNING",
                    "INFO",
                    "DEBUG",
                    "CRITICAL",
                    "Processing",
                    "Created",
                    "Loaded",
                    "Saved",
                    "Generated",
                    "Completed",
                    "Starting",
                    "Finished",
                ],
            )
        ],
    )

    # Get phantom_visuals logger
    logger = logging.getLogger("phantom_visuals")

    # Add file handler
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level.upper())
    logger.addHandler(file_handler)

    # Capture warnings if enabled
    if capture_warnings:
        logging.captureWarnings(True)

    # Log startup message with beautiful formatting
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    startup_panel = Panel(
        f"[info]Phantom Visuals[/info] initialized at [time]{timestamp}[/time]\n"
        f"[subheader]Log Level:[/subheader] [highlight]{level.upper()}[/highlight]   "
        f"[subheader]Log File:[/subheader] [filename]{log_path}[/filename]",
        title="[phantom]✧ PHANTOM VISUALS ✧[/phantom]",
        border_style="cyan",
        box=box.ROUNDED,
        expand=False,
        padding=(1, 2),
    )

    console.print(startup_panel)

    # Simple log message for the file log
    logger.info(f"Logging configured at level {level.upper()}. Log file: {log_path}")

    return logger


def log_config(logger: logging.Logger, config: dict[str, Any]) -> None:
    """Log configuration parameters.

    Args:
        logger: Logger instance
        config: Configuration dictionary to log
    """
    # Create a table for the configuration
    table = Table(
        title="[header]Configuration Parameters[/header]",
        box=box.ROUNDED,
        border_style="cyan",
        title_style="header",
        header_style="subheader",
        row_styles=["", "dim"],
        highlight=True,
        expand=False,
        show_header=True,
    )

    table.add_column("Parameter", style="parameter")
    table.add_column("Value", style="value")

    # Add rows for top-level parameters
    for key, value in config.items():
        # Format nested dictionaries specially
        if isinstance(value, dict):
            value_str = json.dumps(value, indent=2)
            table.add_row(key, f"{value_str}")
        else:
            table.add_row(key, f"{value}")

    console.print(table)

    # Also log to file in a simpler format
    logger.info("Configuration parameters:")
    for key, value in config.items():
        logger.info(f"  {key}: {value}")


def log_cli_command(logger: logging.Logger, command: str, args: dict[str, Any]) -> None:
    """Log CLI command execution.

    Args:
        logger: Logger instance
        command: Command name
        args: Command arguments
    """
    # Create a stylish panel for the command
    cmd_panel = Panel(
        f"[bold]Command:[/bold] [highlight]{command}[/highlight]",
        title="[phantom]Command Execution[/phantom]",
        border_style="cyan",
        box=box.ROUNDED,
        expand=False,
    )

    console.print(cmd_panel)

    # Create a table for the command parameters
    table = Table(
        title="[subheader]Command Parameters[/subheader]",
        box=box.ROUNDED,
        border_style="cyan",
        row_styles=["", "dim"],
        highlight=True,
        expand=False,
        show_header=True,
    )

    table.add_column("Parameter", style="parameter")
    table.add_column("Value", style="value")

    # Add rows for parameters
    for key, value in args.items():
        # Format special values
        if value is None:
            formatted_value = "[dim italic]None[/dim italic]"
        elif isinstance(value, bool):
            formatted_value = "[green]True[/green]" if value else "[red]False[/red]"
        elif isinstance(value, (int, float)):
            formatted_value = f"[bright_cyan]{value}[/bright_cyan]"
        elif isinstance(value, Path):
            formatted_value = f"[filename]{value}[/filename]"
        else:
            formatted_value = f"{value}"

        table.add_row(key, formatted_value)

    console.print(table)

    # Also log to file in a simpler format
    logger.info(f"Executing command: {command}")
    logger.info("Command parameters:")
    for key, value in args.items():
        logger.info(f"  {key}: {value}")


def log_warning(
    logger: logging.Logger, message: str, details: Optional[dict[str, Any]] = None
) -> None:
    """Log a warning message with optional details.

    Args:
        logger: Logger instance
        message: Warning message
        details: Additional details to log
    """
    # Create a warning panel
    details_str = ""
    if details:
        details_str = "\n\n[bold]Details:[/bold]\n"
        for key, value in details.items():
            details_str += f"  [parameter]{key}:[/parameter] {value}\n"

    warning_panel = Panel(
        f"[warning]{message}[/warning]{details_str}",
        title="[phantom]⚠ WARNING[/phantom]",
        border_style="yellow",
        box=box.ROUNDED,
        expand=False,
    )

    console.print(warning_panel)

    # Also log to file
    logger.warning(f"Warning: {message}")  # Use the logger's warning level
    if details:
        for key, value in details.items():
            logger.warning(f"  Detail - {key}: {value}")


def log_error(
    logger: logging.Logger, error: Exception, context: Optional[dict[str, Any]] = None
) -> None:
    """Log an error with context.

    Args:
        logger: Logger instance
        error: Exception to log
        context: Additional context information
    """
    # Create an error panel
    error_message = f"[bold red]{type(error).__name__}:[/bold red] {error!s}"

    # Add context if provided
    context_str = ""
    if context:
        context_str = "\n\n[bold]Context:[/bold]\n"
        for key, value in context.items():
            context_str += f"  [parameter]{key}:[/parameter] {value}\n"

    error_panel = Panel(
        f"{error_message}{context_str}",
        title="[phantom]ERROR[/phantom]",
        border_style="red",
        box=box.HEAVY,
        expand=False,
    )

    console.print(error_panel)

    # Also log to file
    if context:
        logger.error(f"Error occurred with context: {json.dumps(context)}")
    logger.error(f"Error: {error!s}", exc_info=True)


def log_success(
    logger: logging.Logger, message: str, details: Optional[dict[str, Any]] = None
) -> None:
    """Log a success message with optional details.

    Args:
        logger: Logger instance
        message: Success message
        details: Additional details to log
    """
    # Create a success panel
    details_str = ""
    if details:
        details_str = "\n\n"
        for key, value in details.items():
            details_str += f"[parameter]{key}:[/parameter] [value]{value}[/value]\n"

    success_panel = Panel(
        f"[success]{message}[/success]{details_str}",
        title="[phantom]✓ SUCCESS[/phantom]",
        border_style="green",
        box=box.ROUNDED,
        expand=False,
    )

    console.print(success_panel)

    # Also log to file
    logger.info(f"Success: {message}")
    if details:
        for key, value in details.items():
            logger.info(f"  {key}: {value}")


def log_processing_step(
    logger: logging.Logger, step_name: str, description: str = ""
) -> None:
    """Log a processing step.

    Args:
        logger: Logger instance
        step_name: Name of the processing step
        description: Optional description of the step
    """
    step_text = f"[processing]{step_name}[/processing]"
    if description:
        step_text += f"\n[caption]{description}[/caption]"

    console.print(f"[bright_blue]→[/bright_blue] {step_text}")

    # Also log to file
    logger.info(f"Processing step: {step_name}")
    if description:
        logger.info(f"  Description: {description}")


def get_logger() -> logging.Logger:
    """Get the phantom_visuals logger.

    Returns:
        Logger instance
    """
    return logging.getLogger("phantom_visuals")


def create_progress_bar(
    description: str = "Processing",
    total: Optional[float] = None,
    transient: bool = False,
) -> Progress:
    """Create a customized progress bar for phantom-visuals.

    Args:
        description: Description of the progress bar
        total: Total number of steps (None for indeterminate)
        transient: Whether to remove the progress bar after completion

    Returns:
        Rich Progress instance
    """
    return Progress(
        "[time]{task.completed:.0f}/{task.total:.0f}[/time]",
        SpinnerColumn("dots", style="bright_cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="phantom", finished_style="success"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn(
            "[progress.remaining]Remaining: {task.remaining}s[/progress.remaining]"
        ),
        console=console,
        transient=transient,
        expand=True,
    )
