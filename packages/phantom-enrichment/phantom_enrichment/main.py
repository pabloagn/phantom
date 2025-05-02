# phantom_enrichment/main.py

import typer
from typing_extensions import Annotated
from pathlib import Path
from loguru import logger # Import logger after config

from phantom_enrichment.cli import commands

# Initialize logging (will run setup_logging from logging_config)
from .utils import logging_config # noqa

app = typer.Typer(
    name="phantom-enrichment",
    help="Enrichment engine for your personal media library.",
    add_completion=False,
)

# Add command groups or individual commands here
app.add_typer(commands.app, name="enrich")


@app.callback()
def main_callback():
    """
    Main entry point callback for the CLI application.
    """
    # You can add global options or setup here if needed in the future
    pass

if __name__ == "__main__":
    # This allows running the script directly for debugging,
    # but the entry point is typically via the poetry script `phantom-enrichment`
    app()