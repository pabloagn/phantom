# phantom_enrichment/config/settings.py

import os
import sys
import json
from pathlib import Path
from typing import Literal, Dict, List, Any, Optional, Union

# Import loguru here BUT use it carefully before full setup is confirmed
from loguru import logger

from pydantic import (
    Field, SecretStr, HttpUrl, ValidationError, AnyHttpUrl,
    DirectoryPath, FilePath, field_validator, ValidationInfo # Use field_validator decorator
)
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- Define ConfigurationError early ---
class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass

# Attempt to import project specific exception if available
try:
    from phantom_enrichment.utils.exceptions import ConfigurationError as ProjectConfigurationError
    ConfigurationError = ProjectConfigurationError
except ImportError:
    pass # Use the locally defined one


# --- Helper Function to Find Project Root ---
def find_project_root_from_config(marker_files=(".env", "pyproject.toml")):
    """Finds the project root directory by searching upwards from this file's location."""
    current_dir = Path(__file__).resolve().parent
    for directory in [current_dir] + list(current_dir.parents):
        for marker in marker_files:
            if (directory / marker).exists():
                return directory
    raise FileNotFoundError(f"Could not determine project root directory. Looked for {marker_files} starting from {current_dir}.")

# --- Determine Project Root and .env Path Early ---
try:
    PROJECT_ROOT = find_project_root_from_config()
    ENV_PATH = PROJECT_ROOT / '.env'
except FileNotFoundError as e:
    print(f"CRITICAL ERROR finding project root: {e}")
    raise ConfigurationError(f"Could not find project root: {e}") from e


# --- Settings Class Definition ---
class Settings(BaseSettings):
    """Application configuration settings."""
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # --- API Keys & URLs ---
    hardcover_api_key: SecretStr = Field(..., validation_alias='HARDCOVER_API_KEY')
    hardcover_api_url: AnyHttpUrl = Field(..., validation_alias='HARDCOVER_API_URL')
    isbndb_api_key: SecretStr = Field(..., validation_alias='ISBNDB_API_KEY')
    isbndb_base_url: AnyHttpUrl = Field("https://api2.isbndb.com", validation_alias='ISBNDB_BASE_URL')

    # --- General Settings ---
    log_level: str = Field("INFO", validation_alias='LOG_LEVEL')

    # --- File Paths ---
    # Use DirectoryPath for final type check AFTER our pre-validator runs
    input_dir: DirectoryPath = Field(..., validation_alias='INPUT_DIR')
    output_dir: DirectoryPath = Field(..., validation_alias='OUTPUT_DIR')
    log_dir: DirectoryPath = Field(..., validation_alias='LOG_DIR')

    # --- Matching Configuration ---
    matching_type: Literal['exact', 'fuzzy', 'case_insensitive'] = Field(
        "fuzzy", validation_alias='MATCHING_TYPE'
    )
    fuzzy_title_threshold: int = Field(90, ge=0, le=100, validation_alias='FUZZY_TITLE_THRESHOLD')
    fuzzy_author_threshold: int = Field(85, ge=0, le=100, validation_alias='FUZZY_AUTHOR_THRESHOLD')
    initial_search_page_size: int = Field(20, gt=0, le=100, validation_alias='INITIAL_SEARCH_PAGE_SIZE')
    fuzzy_scorer: str = Field("token_sort_ratio", validation_alias='FUZZY_SCORER')


    # --- Properties for calculated paths ---
    @property
    def api_fields_config_path(self) -> FilePath:
        """Calculates the absolute path to the API fields config file."""
        app_dir_name = "phantom_enrichment"
        config_subdir = "config"
        filename = "api_fields.json"
        path = PROJECT_ROOT / app_dir_name / config_subdir / filename
        if not path.is_file():
             raise ConfigurationError(f"API fields configuration file not found at expected location: {path}")
        return path

    @property
    def log_file_path(self) -> Path:
        """Calculates the absolute path to the log file (dir guaranteed to exist by validator)."""
        return self.log_dir / "phantom_enrichment.log"

    # --- CORRECTED Validator for Directory Paths ---
    # Use the newer @field_validator decorator
    # Use mode='before' (V2 equivalent of pre=True)
    # Define as a class method (common pattern) or instance method
    @field_validator('input_dir', 'output_dir', 'log_dir', mode='before')
    @classmethod # Decorate as class method
    def _resolve_and_validate_directories_before(cls, v: Union[str, Path], info: ValidationInfo) -> Path:
        """
        Resolves paths relative to PROJECT_ROOT before standard validation.
        Creates output/log directories if needed.
        Returns a resolved Path object for further validation by DirectoryPath.
        """
        field_name = info.field_name
        if not isinstance(v, (str, Path)):
            raise TypeError(f"Expected str or Path for {field_name}, got {type(v)}")

        path = Path(v)

        # Resolve relative paths using the globally determined PROJECT_ROOT
        if not path.is_absolute():
            if 'PROJECT_ROOT' not in globals():
                 # This should ideally not happen if loading order is correct
                raise ConfigurationError("PROJECT_ROOT not defined when resolving paths.")
            path = PROJECT_ROOT / path

        resolved_path = path.resolve()

        # For output and log directories, ensure they exist (create if needed)
        if field_name in ['output_dir', 'log_dir']:
            try:
                if resolved_path.exists() and not resolved_path.is_dir():
                     raise ValueError(f"Path for {field_name} exists but is not a directory: {resolved_path}")
                resolved_path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise ValueError(f"Failed to create or access directory for {field_name} at {resolved_path}: {e}") from e
            except ValueError as e: # Catch the file-not-dir error
                 raise ValueError(str(e)) # Re-raise with message

        # Return the resolved Path object.
        # Pydantic will then apply the DirectoryPath type validation AFTER this runs.
        return resolved_path


# --- Helper Function to Load API Fields Config ---
def load_api_fields_config(config_path: Path) -> Dict[str, Any]:
    """Loads the API fields config. Uses print for critical errors before logger is ready."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        print(f"INFO: Successfully loaded API fields config from: {config_path}")
        return config_data.get("media_types", {})
    except FileNotFoundError:
        print(f"ERROR: API fields configuration file not found at: {config_path}")
        raise ConfigurationError(f"API fields config missing: {config_path}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Error decoding JSON from API fields config file: {config_path} - {e}")
        raise ConfigurationError(f"Invalid JSON in API fields config: {config_path}")
    except Exception as e:
        print(f"ERROR: Unexpected error loading API fields config: {config_path} - {e}")
        import traceback
        print(f"ERROR DETAILS: {traceback.format_exc()}")
        raise ConfigurationError(f"Failed to load API fields config: {e}")


# --- Instance Creation and Loading ---
settings: Optional[Settings] = None
api_fields_config: Optional[Dict[str, Any]] = None

try:
    # 1. Initialize Pydantic Settings (loads .env, runs validators)
    settings = Settings()

    # 2. Load the API fields JSON config
    api_fields_config = load_api_fields_config(settings.api_fields_config_path)

    print("INFO: Application settings and API fields config loaded successfully.")

    # 3. Trigger main logging configuration
    try:
        from phantom_enrichment.utils import logging_config # noqa
        logger.success("Main logging configuration confirmed after settings load.")
        logger.debug("Settings loaded and logger configured.")
        # logger.trace(f"Loaded settings: {settings.model_dump(exclude={'hardcover_api_key', 'isbndb_api_key'})}")

    except ImportError as e:
         print(f"WARNING: Failed to import logging configuration module: {e}. Main file logging might not work.")
         # Try basic logger setup here if needed
         logger.add(sys.stderr, level="WARNING")
         logger.warning("Using basic stderr logger due to logging config import failure.")
    except Exception as e:
         print(f"WARNING: Unexpected error during logging configuration setup: {e}")
         logger.exception("Logging setup failed.")


except (ValidationError, ConfigurationError) as e:
    # Use PRINT here, as logger setup might have failed or not run yet
    print(f"CRITICAL ERROR during settings/config initialization: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(f"Configuration failed: {e}")

except Exception as e:
    # Catch any other unexpected errors during this critical phase
    print(f"CRITICAL UNEXPECTED ERROR during settings/config initialization: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(f"Unexpected configuration failed: {e}")


# --- Optional Test Block ---
if __name__ == "__main__":
    if not settings or not api_fields_config:
        print("Skipping settings test block due to earlier configuration failure.")
    else:
        # Assuming logger was configured successfully in the main block
        try:
            from loguru import logger # Ensure logger is available in this scope
            logger.info("\n--- Running Settings Test Block ---")
            logger.info(f"Project Root (determined): {PROJECT_ROOT}")
            logger.info(f"Env Path (determined): {ENV_PATH}")
            logger.info(f"Log Level: {settings.log_level}")
            logger.info(f"Input Dir: {settings.input_dir} (Exists: {settings.input_dir.exists()})")
            logger.info(f"Output Dir: {settings.output_dir} (Exists: {settings.output_dir.exists()})")
            logger.info(f"Log Dir: {settings.log_dir} (Exists: {settings.log_dir.exists()})")
            logger.info(f"Log File Path: {settings.log_file_path} (Parent Exists: {settings.log_file_path.parent.exists()})")
            logger.info(f"API Fields Config Path: {settings.api_fields_config_path} (Exists: {settings.api_fields_config_path.exists()})")
            logger.info(f"API Fields Config Loaded: {'Yes' if api_fields_config else 'No'}")
            logger.info(f"--- Matching Params ---")
            logger.info(f"Type: {settings.matching_type}")
            logger.info(f"Title Threshold: {settings.fuzzy_title_threshold}")
            logger.info(f"Author Threshold: {settings.fuzzy_author_threshold}")
            logger.info(f"Initial Page Size: {settings.initial_search_page_size}")
            logger.info(f"Fuzzy Scorer: {settings.fuzzy_scorer}")
            logger.info("--- Test complete ---")
        except NameError:
            print("Logger not available for test block - logging configuration likely failed.")
        except Exception as e:
            print(f"Error during settings test block: {e}")