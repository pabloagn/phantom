# phantom_canon/file_io.py
import logging
import pathlib
from typing import List, Optional, Set

import pandas as pd
import pyarrow as pa

from phantom_canon import constants

log = logging.getLogger(__name__)

# --- Functions (load_excel_sheet, save_raw_parquet_checkpoint, load_parquet, save_parquet) ---
def load_excel_sheet(
    sheet_name: str, expected_columns: Optional[List[str]] = None
    ) -> Optional[pd.DataFrame]:
    """Loads data from a sheet in the main Excel file."""
    excel_file_path: pathlib.Path = constants.EXCEL_FILE
    log.info(f"Attempting to load sheet '{sheet_name}' from '{excel_file_path.name}'...")
    if not excel_file_path.exists():
        log.error(f"Excel file not found at: {excel_file_path}")
        return None
    try:
        df = pd.read_excel(
            excel_file_path, sheet_name=sheet_name, engine="openpyxl"
        )
        log.info(f"Successfully loaded sheet '{sheet_name}'. Found {len(df)} rows, {len(df.columns)} columns.")
        df.columns = df.columns.str.strip()
        if expected_columns:
            expected_columns_stripped = [col.strip() for col in expected_columns]
            missing_cols = [
                col for col in expected_columns_stripped if col not in df.columns
            ]
            if missing_cols:
                log.warning(
                    f"Sheet '{sheet_name}' is missing expected columns: {missing_cols}"
                )
        return df
    except ValueError as ve:
        if f"Worksheet named '{sheet_name}' not found" in str(ve):
            log.error(f"Sheet '{sheet_name}' not found in the Excel file.")
        else:
            log.error(f"An error occurred loading sheet '{sheet_name}': {ve}", exc_info=True)
        return None
    except Exception as e:
        log.error(f"An unexpected error occurred loading sheet '{sheet_name}': {e}", exc_info=True)
        return None

def save_raw_parquet_checkpoint(
    df: pd.DataFrame, parquet_path: pathlib.Path, str_cols: Set[str]
    ) -> bool:
    """Saves a DataFrame to a Parquet file as a raw checkpoint."""
    if df is None:
        log.warning(f"DataFrame is None, cannot save to {parquet_path}.")
        return False
    df_copy = df.copy()
    log.debug(f"Preparing raw save to {parquet_path.name}. Converting columns to string: {str_cols}")
    for col in str_cols:
        if col in df_copy.columns:
            try:
                df_copy[col] = df_copy[col].astype("string")
            except Exception:
                 log.warning(f"Could not convert column '{col}' to 'string' dtype, using .astype(str).", exc_info=False) # Less verbose warning
                 df_copy[col] = df_copy[col].astype(str)
        else:
            log.warning(f"Column '{col}' for string conversion not found in DataFrame for {parquet_path.name}.")
    return save_parquet(df_copy, parquet_path)


def load_parquet(parquet_path: pathlib.Path) -> Optional[pd.DataFrame]:
    """Loads data from a Parquet file."""
    if not parquet_path.is_file():
        log.warning(f"Parquet file not found: {parquet_path}. Returning None.")
        return None
    try:
        log.info(f"Loading data from {parquet_path.name}...")
        df = pd.read_parquet(parquet_path)
        log.info(f"Successfully loaded {len(df)} rows from {parquet_path.name}.")
        return df
    except Exception as e:
        log.error(f"Failed to load Parquet file {parquet_path}: {e}", exc_info=True)
        return None


def save_parquet(df: pd.DataFrame, parquet_path: pathlib.Path) -> bool:
    """Saves a DataFrame to a Parquet file. Assumes dtypes are correct."""
    if df is None:
        log.warning(f"DataFrame is None, cannot save to {parquet_path}.")
        return False
    try:
        log.info(f"Saving {len(df)} rows to {parquet_path.name}...")
        # log.debug(f"dtypes: {df.dtypes.to_dict()}") # Optional: Log dtypes before saving
        parquet_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(parquet_path, index=False, engine="pyarrow")
        log.info(f"Successfully saved data to {parquet_path}.")
        return True
    except pa.lib.ArrowTypeError as ate:
         log.error(f"ArrowTypeError saving {parquet_path}: {ate}. Check DataFrame dtypes.", exc_info=True)
         # Add more specific dtype debugging if needed
         return False
    except Exception as e:
        log.error(f"Failed to save Parquet file {parquet_path}: {e}", exc_info=True)
        return False