# main.py
import logging
import pathlib
import sys
import time
from typing import Dict, List, Optional, Tuple

import pandas as pd

# Use absolute imports based on the CORRECT package structure
from phantom_canon import constants, file_io, cli_display
from phantom_canon.processing import people_processor
from phantom_canon.processing import books_processor
from phantom_canon.processing import films_processor
# from phantom_canon.processing import ... other processors

# --- Configuration ---
LOG_LEVEL = "INFO"
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[cli_display.get_rich_logger_handler(level=LOG_LEVEL)]
)
log = logging.getLogger(__name__)

# --- Helper Function for Reference Loading ---

def _load_and_save_reference(
    sheet_name: str,
    parquet_path: pathlib.Path,
    id_col_name: str,
    rename_map: Optional[Dict[str, str]] = None,
    expected_cols: Optional[List[str]] = None
) -> Tuple[Optional[pd.DataFrame], bool]:
    """Loads a reference sheet, adds ID, renames, saves, returns DataFrame."""
    task_name = f"Load Reference: {sheet_name}"
    cli_display.task_start(task_name)
    df_ref = file_io.load_excel_sheet(sheet_name=sheet_name, expected_columns=expected_cols)
    success = False
    if df_ref is not None and not df_ref.empty:
        cli_display.task_success(task_name, f"Loaded {len(df_ref)} rows")
        cli_display.print_filename(str(constants.EXCEL_FILE))
        save_task_name = f"Save Reference: {parquet_path.name}"
        cli_display.task_start(save_task_name)
        df_ref.columns = df_ref.columns.str.strip()
        if rename_map:
            df_ref = df_ref.rename(columns=rename_map)
        if id_col_name not in df_ref.columns:
            df_ref = df_ref.reset_index().rename(columns={"index": id_col_name})
            df_ref[id_col_name] = df_ref[id_col_name] + constants.ID_START
        else:
            log.warning(f"ID column '{id_col_name}' already exists in sheet '{sheet_name}'. Using existing IDs.")
        df_ref[id_col_name] = pd.to_numeric(df_ref[id_col_name], errors='coerce').astype('Int64')
        df_ref = df_ref.dropna(subset=[id_col_name])
        if rename_map:
             final_cols = [id_col_name] + list(rename_map.values())
             df_ref = df_ref[[col for col in final_cols if col in df_ref.columns]]
        if file_io.save_parquet(df_ref, parquet_path):
            cli_display.task_success(save_task_name)
            cli_display.print_filename(str(parquet_path))
            success = True
        else:
            cli_display.task_failure(save_task_name)
    elif df_ref is not None and df_ref.empty:
         cli_display.task_warning(f"{task_name}: Sheet is empty.")
         success = True
    else:
        cli_display.task_failure(task_name)
    return df_ref, success

# --- Main Application Logic ---

def initial_excel_load() -> bool:
    """Loads data from Excel sheets and saves raw parquet checkpoints & reference tables."""
    cli_display.print_sub_header("Stage 1: Initial Load from Excel")
    overall_success = True
    tasks_failed = []

    # --- Load People (Raw) ---
    task_name = "Load People (Raw)"
    df_people_raw = file_io.load_excel_sheet(
        sheet_name=constants.SHEET_PEOPLE,
        expected_columns=constants.PEOPLE_EXCEL_COLS_NEEDED
    )
    if df_people_raw is not None:
        cli_display.task_success(task_name, f"Loaded {len(df_people_raw)} rows")
        cli_display.print_filename(str(constants.EXCEL_FILE))
        save_task_name = "Save raw People checkpoint"
        cli_display.task_start(save_task_name)
        if file_io.save_raw_parquet_checkpoint(
            df_people_raw, constants.PEOPLE_RAW_PQ, constants.PEOPLE_RAW_SAVE_STR_COLS
        ):
            cli_display.task_success(save_task_name)
            cli_display.print_filename(str(constants.PEOPLE_RAW_PQ))
        else:
            cli_display.task_failure(save_task_name)
            tasks_failed.append(save_task_name)
            overall_success = False
    else:
        cli_display.task_failure(task_name)
        tasks_failed.append(task_name)
        overall_success = False

    # --- Load Books (Raw) ---
    task_name = "Load Books (Raw)"
    df_books_raw = file_io.load_excel_sheet(
        sheet_name=constants.SHEET_BOOKS,
        expected_columns=constants.BOOKS_EXCEL_COLS_NEEDED
    )
    if df_books_raw is not None:
        cli_display.task_success(task_name, f"Loaded {len(df_books_raw)} rows")
        cli_display.print_filename(str(constants.EXCEL_FILE))
        save_task_name = "Save raw Books checkpoint"
        cli_display.task_start(save_task_name)
        if file_io.save_raw_parquet_checkpoint(
            df_books_raw, constants.BOOKS_RAW_PQ, constants.BOOKS_RAW_SAVE_STR_COLS
        ):
             cli_display.task_success(save_task_name)
             cli_display.print_filename(str(constants.BOOKS_RAW_PQ))
        else:
            cli_display.task_failure(save_task_name)
            tasks_failed.append(save_task_name)
            overall_success = False
    else:
        cli_display.task_warning(f"{task_name} failed or sheet empty.")
        tasks_failed.append(task_name)
        overall_success = False

    # --- Load Films (Raw) ---
    task_name = "Load Films (Raw)"
    df_films_raw = file_io.load_excel_sheet(
        sheet_name=constants.SHEET_FILMS,
        expected_columns=constants.FILMS_EXCEL_COLS_NEEDED
    )
    if df_films_raw is not None:
        cli_display.task_success(task_name, f"Loaded {len(df_films_raw)} rows")
        cli_display.print_filename(str(constants.EXCEL_FILE))
        save_task_name = "Save raw Films checkpoint"
        cli_display.task_start(save_task_name)
        if file_io.save_raw_parquet_checkpoint(
            df_films_raw, constants.FILMS_RAW_PQ, constants.FILMS_RAW_SAVE_STR_COLS
        ):
             cli_display.task_success(save_task_name)
             cli_display.print_filename(str(constants.FILMS_RAW_PQ))
        else:
            cli_display.task_failure(save_task_name)
            tasks_failed.append(save_task_name)
            overall_success = False
    else:
        cli_display.task_warning(f"{task_name} failed or sheet empty.")
        tasks_failed.append(task_name)
        overall_success = False

    # --- Load Reference Tables ---
    cli_display.print_sub_header("Stage 1b: Loading Reference Tables")
    # Countries
    _, success = _load_and_save_reference(
        sheet_name=constants.SHEET_COUNTRIES, parquet_path=constants.COUNTRIES_PQ, id_col_name=constants.COUNTRY_ID,
        rename_map={ constants.EXCEL_COUNTRY_NAME: constants.COUNTRY_NAME, constants.EXCEL_COUNTRY_ALPHA2: constants.COUNTRY_ISO_ALPHA2, constants.EXCEL_COUNTRY_ALPHA3: constants.COUNTRY_ISO_ALPHA3, constants.EXCEL_COUNTRY_NUMBER: constants.COUNTRY_NUMBER_COL, constants.EXCEL_COUNTRY_CONTINENT_CODE: constants.COUNTRY_CONTINENT_CODE, constants.EXCEL_COUNTRY_CONTINENT_NAME: constants.COUNTRY_CONTINENT_NAME,},
        expected_cols=[constants.EXCEL_COUNTRY_NAME, constants.EXCEL_COUNTRY_ALPHA2] )
    if not success: tasks_failed.append(f"Load/Save {constants.SHEET_COUNTRIES}"); overall_success = False
    # Languages
    _, success = _load_and_save_reference(
        sheet_name=constants.SHEET_LANGUAGES, parquet_path=constants.LANGUAGES_PQ, id_col_name=constants.LANGUAGE_ID,
        rename_map={ constants.EXCEL_LANG_NAME: constants.LANGUAGE_NAME, constants.EXCEL_LANG_ISO1: constants.LANGUAGE_ISO1, constants.EXCEL_LANG_ISO2: constants.LANGUAGE_ISO2, constants.EXCEL_LANG_ISO3: constants.LANGUAGE_ISO3,},
        expected_cols=[constants.EXCEL_LANG_NAME] )
    if not success: tasks_failed.append(f"Load/Save {constants.SHEET_LANGUAGES}"); overall_success = False
    # Work Types
    _, success = _load_and_save_reference(
        sheet_name=constants.SHEET_WORK_TYPES, parquet_path=constants.WORK_TYPES_PQ, id_col_name=constants.WORK_TYPE_ID,
        rename_map={ constants.EXCEL_WORK_TYPE_NAME: constants.WORK_TYPE_NAME, }, expected_cols=[constants.EXCEL_WORK_TYPE_NAME] )
    if not success: tasks_failed.append(f"Load/Save {constants.SHEET_WORK_TYPES}"); overall_success = False
    # Contribution Types
    _, success = _load_and_save_reference(
        sheet_name=constants.SHEET_CONTRIBUTION_TYPES, parquet_path=constants.CONTRIBUTION_TYPES_PQ, id_col_name=constants.CONTRIB_TYPE_ID,
        rename_map={ constants.EXCEL_CONTRIB_TYPE_NAME: constants.CONTRIB_TYPE_NAME, }, expected_cols=[constants.EXCEL_CONTRIB_TYPE_NAME] )
    if not success: tasks_failed.append(f"Load/Save {constants.SHEET_CONTRIBUTION_TYPES}"); overall_success = False

    if not overall_success: log.error(f"Initial Load Stage completed with failures: {tasks_failed}")
    else: log.info("--- Initial Load Stage completed successfully ---")
    return overall_success


def process_data() -> bool:
    """Loads raw data from parquet, processes it, and saves final parquet files."""
    cli_display.print_sub_header("Stage 2: Processing Data")
    overall_success = True
    tasks_failed = []
    all_processed_works = []
    all_processed_contributors = []
    next_work_id = constants.ID_START

    # --- Load Reference Data ---
    cli_display.task_start("Loading reference data (Parquet)")
    df_countries = file_io.load_parquet(constants.COUNTRIES_PQ)
    df_languages = file_io.load_parquet(constants.LANGUAGES_PQ)
    df_work_types = file_io.load_parquet(constants.WORK_TYPES_PQ)
    df_contrib_types = file_io.load_parquet(constants.CONTRIBUTION_TYPES_PQ)
    if df_countries is None or df_languages is None or df_work_types is None or df_contrib_types is None:
        log.error("One or more critical reference Parquet files failed to load. Aborting processing.")
        cli_display.task_failure("Loading reference data (Parquet)")
        return False
    cli_display.task_success("Loading reference data (Parquet)")

    # --- Create Reference Lookups ---
    cli_display.task_start("Creating reference lookups")
    try:
        lang_lookup = df_languages.set_index(df_languages[constants.LANGUAGE_NAME].str.lower().str.strip())[constants.LANGUAGE_ID].to_dict()
        work_type_lookup = df_work_types.set_index(df_work_types[constants.WORK_TYPE_NAME].str.lower().str.strip())[constants.WORK_TYPE_ID].to_dict()
        contrib_type_lookup = df_contrib_types.set_index(df_contrib_types[constants.CONTRIB_TYPE_NAME].str.lower().str.strip())[constants.CONTRIB_TYPE_ID].to_dict()
        cli_display.task_success("Creating reference lookups")
    except Exception as e:
        log.error(f"Failed to create reference lookups: {e}")
        cli_display.task_failure("Creating reference lookups")
        cli_display.print_exception()
        return False

    # --- Process People ---
    process_task_name = "Process People Data"
    cli_display.task_start(process_task_name)
    df_people_raw = file_io.load_parquet(constants.PEOPLE_RAW_PQ)
    df_people_final = None
    df_person_nationalities = None
    if df_people_raw is not None:
        try:
            df_people_final, df_person_nationalities = people_processor.process_people(df_people_raw, df_countries)
            if df_people_final is not None:
                 cli_display.task_success(process_task_name, f"Processed {len(df_people_final)} people")
                 save_task_name = "Save final People parquet"
                 cli_display.task_start(save_task_name)
                 if file_io.save_parquet(df_people_final, constants.PEOPLE_PQ):
                     cli_display.task_success(save_task_name); cli_display.print_filename(str(constants.PEOPLE_PQ))
                 else:
                     cli_display.task_failure(save_task_name); tasks_failed.append(save_task_name); overall_success = False
            else:
                 cli_display.task_failure(process_task_name, "Processing function returned None for People"); tasks_failed.append(process_task_name); overall_success = False
            if df_person_nationalities is not None and not df_person_nationalities.empty:
                 save_task_name = "Save Person Nationalities parquet"
                 cli_display.task_start(save_task_name)
                 if file_io.save_parquet(df_person_nationalities, constants.PERSON_NATIONALITIES_PQ):
                      cli_display.task_success(save_task_name, f"Saved {len(df_person_nationalities)} links"); cli_display.print_filename(str(constants.PERSON_NATIONALITIES_PQ))
                 else:
                      cli_display.task_failure(save_task_name); tasks_failed.append(save_task_name); overall_success = False
            else:
                 cli_display.print_info("Person Nationalities processing returned None or empty DataFrame.")
        except Exception as e:
             cli_display.task_failure(process_task_name, "An exception occurred during processing")
             log.error(f"Error processing people data: {e}"); cli_display.print_exception(); tasks_failed.append(process_task_name); overall_success = False
    else:
        cli_display.task_warning("Skipping People processing", "Raw Parquet file not found."); tasks_failed.append(process_task_name + " (skipped)"); overall_success = False

    # --- Create People Lookups ---
    people_lookup = {}
    people_display_lookup = {}
    if df_people_final is not None and overall_success:
        cli_display.task_start("Creating People lookups")
        try:
            people_lookup = df_people_final.set_index(df_people_final[constants.PERSON_SORT_NAME].str.lower().str.strip())[constants.PERSON_ID].to_dict()
            temp_people_display = df_people_final[[constants.PERSON_DISPLAY_NAME, constants.PERSON_ID]].copy()
            temp_people_display['lookup_key'] = temp_people_display[constants.PERSON_DISPLAY_NAME].str.lower().str.strip()
            temp_people_display = temp_people_display.drop_duplicates(subset=['lookup_key'], keep='first')
            people_display_lookup = temp_people_display.set_index('lookup_key')[constants.PERSON_ID].to_dict()
            cli_display.task_success(f"Creating People lookups (Sort: {len(people_lookup)}, Display: {len(people_display_lookup)})")
            del temp_people_display
        except Exception as e:
            log.error(f"Failed to create People lookups: {e}"); cli_display.task_failure("Creating People lookups"); cli_display.print_exception(); overall_success = False

    # --- Process Books ---
    if overall_success:
        process_task_name = "Process Books Data"
        cli_display.task_start(process_task_name)
        df_books_raw = file_io.load_parquet(constants.BOOKS_RAW_PQ)
        if df_books_raw is not None and df_people_final is not None:
            try:
                df_books_works, df_books_contribs, next_work_id = books_processor.process_books(
                    df_raw_books=df_books_raw, people_lookup=people_lookup, people_display_lookup=people_display_lookup,
                    lang_lookup=lang_lookup, work_type_lookup=work_type_lookup, contrib_type_lookup=contrib_type_lookup, start_work_id=next_work_id )
                if df_books_works is not None:
                    all_processed_works.append(df_books_works); cli_display.task_success(process_task_name, f"Generated {len(df_books_works)} Book Works")
                else:
                    cli_display.task_failure(process_task_name, "Processing returned None for Book Works"); tasks_failed.append(process_task_name + " (Works)"); overall_success = False
                if df_books_contribs is not None and not df_books_contribs.empty:
                    all_processed_contributors.append(df_books_contribs); cli_display.task_success(process_task_name, f"Generated {len(df_books_contribs)} Book Contributors")
                else:
                     cli_display.print_info("No contributors generated for Books.")
            except Exception as e:
                cli_display.task_failure(process_task_name, "An exception occurred"); log.error(f"Error processing book data: {e}"); cli_display.print_exception(); tasks_failed.append(process_task_name); overall_success = False
        else:
             cli_display.task_warning(f"Skipping {process_task_name}", "Raw Books or Processed People Parquet not available."); tasks_failed.append(process_task_name + " (skipped)"); overall_success = False

    # --- Process Films ---
    if overall_success:
        process_task_name = "Process Films Data"
        cli_display.task_start(process_task_name)
        df_films_raw = file_io.load_parquet(constants.FILMS_RAW_PQ)
        if df_films_raw is not None and df_people_final is not None:
            try:
                df_films_works, df_films_contribs, next_work_id = films_processor.process_films(
                    df_raw_films=df_films_raw, people_lookup=people_lookup, people_display_lookup=people_display_lookup,
                    lang_lookup=lang_lookup, work_type_lookup=work_type_lookup, contrib_type_lookup=contrib_type_lookup, start_work_id=next_work_id )
                if df_films_works is not None:
                    all_processed_works.append(df_films_works); cli_display.task_success(process_task_name, f"Generated {len(df_films_works)} Film Works")
                else:
                    cli_display.task_failure(process_task_name, "Processing returned None for Film Works"); tasks_failed.append(process_task_name + " (Works)"); overall_success = False
                if df_films_contribs is not None and not df_films_contribs.empty:
                    all_processed_contributors.append(df_films_contribs); cli_display.task_success(process_task_name, f"Generated {len(df_films_contribs)} Film Contributors")
                else:
                     cli_display.print_info("No contributors generated for Films.")
            except Exception as e:
                cli_display.task_failure(process_task_name, "An exception occurred"); log.error(f"Error processing film data: {e}"); cli_display.print_exception(); tasks_failed.append(process_task_name); overall_success = False
        else:
             cli_display.task_warning(f"Skipping {process_task_name}", "Raw Films or Processed People Parquet not available."); tasks_failed.append(process_task_name + " (skipped)"); overall_success = False

    # --- Combine and Save Final Works and Contributors ---
    if overall_success:
        cli_display.print_sub_header("Stage 2b: Finalizing Processed Data")
        if all_processed_works:
            df_works_final = pd.concat(all_processed_works, ignore_index=True)
            save_task_name = "Save final Works parquet"
            cli_display.task_start(save_task_name)
            if file_io.save_parquet(df_works_final, constants.WORKS_PQ):
                cli_display.task_success(save_task_name, f"Saved {len(df_works_final)} total works"); cli_display.print_filename(str(constants.WORKS_PQ))
            else:
                cli_display.task_failure(save_task_name); tasks_failed.append(save_task_name); overall_success = False
        else:
            cli_display.task_warning("No works data processed to save.")
        if all_processed_contributors:
            df_contributors_final = pd.concat(all_processed_contributors, ignore_index=True)
            df_contributors_final = df_contributors_final.astype({ constants.CONTRIB_WORK_ID: 'Int64', constants.CONTRIB_PERSON_ID: 'Int64', constants.CONTRIB_CONTRIB_TYPE_ID: 'Int64', })
            save_task_name = "Save final Work Contributors parquet"
            cli_display.task_start(save_task_name)
            if file_io.save_parquet(df_contributors_final, constants.WORK_CONTRIBUTORS_PQ):
                cli_display.task_success(save_task_name, f"Saved {len(df_contributors_final)} total contributor links"); cli_display.print_filename(str(constants.WORK_CONTRIBUTORS_PQ))
            else:
                cli_display.task_failure(save_task_name); tasks_failed.append(save_task_name); overall_success = False
        else:
            cli_display.task_warning("No contributor data processed to save.")

    if not overall_success: log.error(f"Data Processing Stage completed with failures: {tasks_failed}")
    else: log.info("--- Data Processing Stage completed successfully ---")
    return overall_success


def main():
    """Main function to run the ETL pipeline."""
    cli_display.print_header("Phantom Canon - Data Processing Pipeline")
    start_time = time.time()
    overall_success = False
    try:
        if initial_excel_load():
            if process_data():
                overall_success = True
    except Exception as e:
        log.critical(f"Critical error in main execution flow: {e}"); cli_display.print_exception(); overall_success = False
    finally:
        duration = time.time() - start_time
        cli_display.print_summary(duration, overall_success)
        sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    main()