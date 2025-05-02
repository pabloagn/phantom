      
# phantom_enrichment/datasources/excel_handler.py

import pandas as pd
from pathlib import Path
from loguru import logger
from typing import Optional

from phantom_enrichment.utils.exceptions import DataSourceError

class ExcelHandler:
    """Handles reading from and writing to Excel files."""

    @staticmethod
    def read_excel(file_path: Path, sheet_name: Optional[str | int] = 0) -> pd.DataFrame:
        """
        Reads data from an Excel file into a pandas DataFrame.

        Args:
            file_path: Path to the input Excel file (.xlsx).
            sheet_name: Name or index of the sheet to read (default is the first sheet).

        Returns:
            A pandas DataFrame containing the data.

        Raises:
            DataSourceError: If the file cannot be read or is not found.
            ValueError: If the specified sheet doesn't exist.
        """
        logger.info(f"Attempting to read Excel file: {file_path}, Sheet: {sheet_name}")
        if not file_path.exists():
            msg = f"Input Excel file not found at: {file_path}"
            logger.error(msg)
            raise DataSourceError(msg)

        try:
            # Use openpyxl engine for .xlsx files
            df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
            logger.success(f"Successfully read {len(df)} rows from {file_path}")
            # Basic validation: Log columns found
            logger.debug(f"Columns found in input: {df.columns.tolist()}")
            return df
        except FileNotFoundError:
            # This case should be caught by the initial check, but added for safety
            msg = f"Input Excel file not found (pd.read_excel): {file_path}"
            logger.error(msg)
            raise DataSourceError(msg)
        except ValueError as e:
            # Pandas raises ValueError if sheet_name doesn't exist
            msg = f"Sheet '{sheet_name}' not found in Excel file {file_path}: {e}"
            logger.error(msg)
            raise DataSourceError(msg)
        except Exception as e:
            msg = f"Failed to read Excel file {file_path}: {e}"
            logger.exception(msg) # Log full traceback
            raise DataSourceError(msg) from e

    @staticmethod
    def save_dataframe_to_excel(df: pd.DataFrame, file_path: Path, sheet_name: str = 'Enriched Data'):
        """
        Saves a pandas DataFrame to an Excel file (.xlsx).

        Args:
            df: The DataFrame to save.
            file_path: The path where the output Excel file will be saved.
            sheet_name: The name for the sheet in the output file.

        Raises:
            DataSourceError: If the DataFrame cannot be saved.
        """
        logger.info(f"Attempting to save DataFrame ({len(df)} rows) to Excel file: {file_path}, Sheet: {sheet_name}")

        # Ensure output directory exists
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
             msg = f"Failed to create output directory {file_path.parent}: {e}"
             logger.error(msg)
             raise DataSourceError(msg) from e

        try:
            # index=False prevents writing the DataFrame index as a column
            df.to_excel(file_path, sheet_name=sheet_name, index=False, engine='openpyxl')
            logger.success(f"Successfully saved DataFrame to {file_path}")
        except Exception as e:
            msg = f"Failed to save DataFrame to Excel file {file_path}: {e}"
            logger.exception(msg)
            raise DataSourceError(msg) from e

# Example usage (optional, for testing)
if __name__ == '__main__':
    # Requires creating dummy files or adjusting paths
    test_input_dir = Path("./test_input")
    test_output_dir = Path("./test_output")
    test_input_dir.mkdir(exist_ok=True)
    test_output_dir.mkdir(exist_ok=True)

    # Create a dummy input file
    dummy_input_path = test_input_dir / "dummy_input.xlsx"
    dummy_df_in = pd.DataFrame({'Title': ['Test Book 1', 'Test Book 2'], 'Author': ['Author A', 'Author B']})
    try:
        ExcelHandler.save_dataframe_to_excel(dummy_df_in, dummy_input_path, sheet_name='Books')
        logger.info(f"Created dummy input file: {dummy_input_path}")

        # Test reading
        read_df = ExcelHandler.read_excel(dummy_input_path, sheet_name='Books')
        logger.info("Read DataFrame:")
        print(read_df)

        # Test saving (different file)
        dummy_output_path = test_output_dir / "dummy_output.xlsx"
        dummy_df_out = read_df.copy()
        dummy_df_out['ISBN13'] = ['9780000000001', '9780000000002']
        ExcelHandler.save_dataframe_to_excel(dummy_df_out, dummy_output_path)
        logger.info(f"Saved dummy output file: {dummy_output_path}")

        # Test reading non-existent file
        try:
             ExcelHandler.read_excel(Path("./non_existent.xlsx"))
        except DataSourceError as e:
             logger.info(f"Caught expected error for non-existent file: {e}")

        # Test reading non-existent sheet
        try:
             ExcelHandler.read_excel(dummy_input_path, sheet_name='WrongSheet')
        except DataSourceError as e:
             logger.info(f"Caught expected error for non-existent sheet: {e}")

    except DataSourceError as e:
        logger.error(f"Error during ExcelHandler test: {e}")
    finally:
         # Clean up dummy files/dirs if needed
         # import shutil
         # if test_input_dir.exists(): shutil.rmtree(test_input_dir)
         # if test_output_dir.exists(): shutil.rmtree(test_output_dir)
         pass