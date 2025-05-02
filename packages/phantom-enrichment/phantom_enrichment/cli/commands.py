# phantom_enrichment/cli/commands.py

import typer
from typing_extensions import Annotated
from typing import Union # Keep Union for internal type hint
from pathlib import Path
from loguru import logger
import pandas as pd
import sys # Import sys for exit on import error

# Import necessary components from the project
# Ensure these imports work based on your project structure and __init__.py files
try:
    from phantom_enrichment.config.settings import settings, api_fields_config # Import loaded settings & config
    from phantom_enrichment.core.orchestrator import Orchestrator
    from phantom_enrichment.datasources.excel_handler import ExcelHandler
    from phantom_enrichment.utils.exceptions import DataSourceError, ConfigurationError, EnrichmentError
except ImportError as e:
     # Provide a more informative error if imports fail during startup
     print(f"CRITICAL IMPORT ERROR in cli/commands.py: {e}")
     print("Ensure all necessary modules exist and __init__.py files are present.")
     # Exit cleanly if essential imports fail
     sys.exit(f"Import failed: {e}")


# Initialize Typer app for the 'enrich' command group
app = typer.Typer(
    help="Enrich media metadata using various configured providers.",
    context_settings={"help_option_names": ["-h", "--help"]} # Add standard help options
)

@app.command("books")
def enrich_books(
    input_file: Annotated[Path, typer.Option(
        "--input", "-i",
        help="Path to the input Excel file (.xlsx) relative to the configured input directory or an absolute path.",
        resolve_path=False, # Keep it as provided by user initially
    )],
    output_filename: Annotated[str, typer.Option(
        "--output", "-o",
        help="Filename for the enriched Excel file (.xlsx) to be saved in the configured output directory. "
             "If not provided, defaults to '[input_file_name]_enriched.xlsx'.",
    )] = None,
    # Accept as string from Typer
    input_sheet_str: Annotated[str, typer.Option(
        "--sheet", "-s",
        help="Name (string) or index (integer, 0-based) of the sheet to read from the input Excel file."
    )] = "0", # Default to string "0"
    providers: Annotated[str, typer.Option(
        "--providers", "-p",
        help="Comma-separated list of providers to use (e.g., 'isbndb'). Default: 'isbndb'.",
    )] = "isbndb",
):
    """
    Enriches book metadata from an input Excel file using configured providers
    (currently supports ISBNDB) and saves the results to a new Excel file.

    Reads 'Title' and 'Author' columns from the input file.
    Produces an output file with detailed edition information for matched books.
    """
    # Logger should be configured by the time this command runs due to settings import
    logger.info("--- Starting Book Enrichment Process ---")

    # --- Convert and validate input_sheet ---
    sheet_to_read: Union[str, int] # Define the type we want internally
    try:
        # Try converting to integer first (for index)
        sheet_to_read = int(input_sheet_str)
        logger.info(f"Input Sheet interpreted as index: {sheet_to_read}")
    except ValueError:
        # If conversion fails, treat it as a sheet name (string)
        sheet_to_read = input_sheet_str
        logger.info(f"Input Sheet interpreted as name: '{sheet_to_read}'")
    # --- End Conversion Block ---


    # --- Resolve Paths using configured directories ---
    resolved_input_path: Optional[Path] = None
    resolved_output_path: Optional[Path] = None
    try:
        # Ensure settings object is available (should be loaded on import)
        if not settings:
             raise ConfigurationError("Settings object not loaded correctly.")

        # Check if input_dir exists before trying to resolve within it
        if not settings.input_dir.exists():
             raise ConfigurationError(f"Configured input directory does not exist: {settings.input_dir}")

        resolved_input_path = settings.input_dir / input_file if not Path(input_file).is_absolute() else Path(input_file)
        logger.info(f"Resolved Input Path: {resolved_input_path}")

        # Check if resolved input path actually exists before proceeding
        if not resolved_input_path.exists():
             raise DataSourceError(f"Input file does not exist at resolved path: {resolved_input_path}")
        if not resolved_input_path.is_file():
             raise DataSourceError(f"Input path is not a file: {resolved_input_path}")


        if output_filename is None:
            # Use stem from the original input_file name as provided by user
            output_filename = f"{Path(input_file).stem}_enriched.xlsx"
        # Output path is resolved relative to output_dir setting
        resolved_output_path = settings.output_dir / output_filename
        logger.info(f"Resolved Output Path: {resolved_output_path}")

        # Ensure output directory exists (settings validator should have created it)
        if not settings.output_dir.exists() or not settings.output_dir.is_dir():
             # This might indicate a problem post-initialization
             logger.warning(f"Output directory {settings.output_dir} not found or not a directory. Attempting to create.")
             try:
                  settings.output_dir.mkdir(parents=True, exist_ok=True)
             except OSError as e:
                  raise ConfigurationError(f"Failed to ensure output directory {settings.output_dir} exists: {e}")


    except ConfigurationError as e:
        logger.critical(f"Configuration error resolving paths: {e}")
        raise typer.Exit(code=1)
    except DataSourceError as e:
         logger.critical(f"Input file error: {e}")
         raise typer.Exit(code=1)
    except Exception as e:
         logger.critical(f"Error resolving input/output paths: {e}")
         logger.exception("Path resolution error details:")
         raise typer.Exit(code=1)


    provider_list = [p.strip().lower() for p in providers.split(',') if p.strip()]
    if not provider_list:
         logger.error("No valid providers specified.")
         raise typer.Exit(code=1)

    # Log the interpreted sheet name/index
    logger.info(f"Will attempt to read sheet: {sheet_to_read}")
    logger.info(f"Providers selected: {provider_list}")


    # --- Core Workflow ---
    try:
        # 1. Load Input Data
        logger.info("Loading input data...")
        # Pass the *converted* sheet_to_read value
        input_df = ExcelHandler.read_excel(resolved_input_path, sheet_name=sheet_to_read)
        logger.info(f"Loaded {len(input_df)} rows from input file.")
        # Add basic check for required columns after loading
        if not all(col in input_df.columns for col in ['Title', 'Author']):
             logger.error("Input DataFrame does not contain required columns: 'Title', 'Author'.")
             raise DataSourceError("Input file missing required columns: 'Title', 'Author'")

        # 2. Initialize Orchestrator
        logger.info("Initializing orchestrator...")
        # Ensure settings and api_fields_config are available
        if not settings or not api_fields_config:
             raise ConfigurationError("Settings or API fields configuration not loaded correctly.")
        orchestrator = Orchestrator(settings=settings, api_fields_config=api_fields_config)

        # 3. Run Enrichment
        logger.info("Starting enrichment process...")
        enriched_df = orchestrator.enrich_books(input_df, providers=provider_list)

        # 4. Save Results
        if enriched_df is not None and not enriched_df.empty:
            logger.info(f"Enrichment successful. Saving {len(enriched_df)} enriched records...")
            ExcelHandler.save_dataframe_to_excel(enriched_df, resolved_output_path)
            logger.success(f"--- Book Enrichment Process Completed Successfully ---")
            logger.info(f"Output saved to: {resolved_output_path}")
        elif enriched_df is not None and enriched_df.empty:
             logger.warning("Enrichment process completed, but no matching editions were found or collected.")
             logger.info("No output file generated.")
        else:
            # This case might occur if orchestrator returns None due to client errors etc.
            logger.error("Enrichment process failed to produce results (returned None). Check logs for details.")
            raise typer.Exit(code=1) # Exit with error if no DataFrame returned

    except (DataSourceError, ConfigurationError, EnrichmentError, ValueError) as e:
        # Catch specific, known application errors
        logger.critical(f"Enrichment failed due to an application error: {e}")
        # Optionally log traceback for these expected errors if needed for debugging
        # logger.exception("Traceback:")
        raise typer.Exit(code=1)
    except ImportError as e:
        # Catch potential import errors missed earlier
        logger.critical(f"Import error during execution: {e}")
        raise typer.Exit(code=1)
    except Exception as e:
        # Catch unexpected errors
        logger.critical(f"An unexpected error occurred during the enrichment process.")
        logger.exception("Unexpected Error Details:") # Log full traceback for unexpected errors
        raise typer.Exit(code=1)


# --- Placeholder for other media types ---
# @app.command("films")
# def enrich_films(...):
#     logger.info("Starting film enrichment process...")
#     # ... implementation ...
#     pass