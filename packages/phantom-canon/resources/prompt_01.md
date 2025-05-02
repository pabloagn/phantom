Developing an app called phantom-canon. Here is the dir structure:

D:.
│   .gitignore
│   main.py
│   poetry.lock
│   processing.log
│   pyproject.toml
│   README.md
│
├───data
│   │   knowledge_base.xlsm
│   │
│   └───parquet_store
│           books_raw_temp.parquet
│           films_raw_temp.parquet
│           people.parquet
│           people_raw_temp.parquet
│           person_nationalities.parquet
│
├───notebooks
│       eda.ipynb
│
├───phantom_canon
│   │   cli_display.py
│   │   constants.py
│   │   file_io.py
│   │   __init__.py
│   │
│   ├───processing
│   │   │   people_processor.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           people_processor.cpython-311.pyc
│   │           __init__.cpython-311.pyc
│   │
│   └───__pycache__
│           cli_display.cpython-311.pyc
│           constants.cpython-311.pyc
│           file_io.cpython-311.pyc
│           __init__.cpython-311.pyc

The purpose of this app is to do as follows:
- I have an xlsm file which contains several tables on separate sheets.
- I also have this schema design:

//// ------------------------------------------------------ ////
////           Phantom DB Schema - dbdiagram.io             ////
//// ------------------------------------------------------ ////

// --- Project Settings (Optional: for dbdiagram.io) ---
Project phantom_db {
  database_type: 'PostgreSQL'
  Note: 'Knowledge repository schema for art, philosophy, etc.'
}

// --- Reference Tables (Controlled Vocabularies & Entities) ---

Table countries {
  country_id integer [pk, increment]
  name varchar(100) [unique, not null]
  iso_alpha2 char(2) [unique]
  iso_alpha3 char(3) [unique]
  country_number integer [unique]
  continent_code char(2)
  continent_name varchar(50)
  Note: 'Stores country information, linked for nationality, birth/death places, publishers.'
  Indexes {
    name // Index on name column
  }
}

Table languages {
  language_id integer [pk, increment]
  name varchar(100) [unique, not null]
  iso_639_1 char(2) [unique]
  iso_639_2 char(3) [unique]
  iso_639_3 char(3) [unique]
  Note: 'Stores language information for works and manifestations.'
  Indexes {
    name // Index on name column
  }
}

Table publishing_houses {
  publisher_id integer [pk, increment]
  name varchar(255) [unique, not null]
  country_id integer [ref: > countries.country_id]
  specialties text
  Note: 'Stores book publishers.'
  Indexes {
    name // Index on name column
  }
}

Table perfume_houses {
  perfume_house_id integer [pk, increment]
  name varchar(255) [unique, not null]
  country_id integer [ref: > countries.country_id]
  Note: 'Stores perfume houses/brands.'
  Indexes {
    name // Index on name column
  }
}

Table work_types {
 work_type_id integer [pk, increment]
 name varchar(100) [unique, not null] // e.g., 'Book', 'Painting', 'Perfume', 'Film'
 Note: 'Defines the primary type of a creative work.'
}

Table contribution_types {
 contribution_type_id integer [pk, increment]
 name varchar(100) [unique, not null] // e.g., 'Author', 'Painter', 'Composer', 'Director', 'Translator'
 Note: 'Defines the roles people can play in relation to a work.'
}


// --- Taxonomy Tables (Hierarchical & Flat Classifications) ---

Table genres {
  genre_id integer [pk, increment]
  name varchar(255) [not null]
  description text
  parent_genre_id integer [ref: > genres.genre_id] // Self-ref for hierarchy
  work_type_scope varchar(100) // Optional filter (e.g., 'Literature', 'Music')
  Indexes {
    (name, parent_genre_id) [unique, name: 'uq_genres_name_parent'] // Composite unique constraint implicitly creates an index
    parent_genre_id // Index on FK for hierarchy lookups
  }
  Note: 'Hierarchical classification of genres (e.g., Fiction > Sci-Fi > Cyberpunk).'
}

Table movements {
  movement_id integer [pk, increment]
  name varchar(255) [not null]
  description text
  period_start integer
  period_end integer
  parent_movement_id integer [ref: > movements.movement_id] // Self-ref for hierarchy
  region varchar(100) // Optional geographic focus
  Indexes {
    (name, parent_movement_id) [unique, name: 'uq_movements_name_parent'] // Composite unique constraint implicitly creates an index
    parent_movement_id // Index on FK for hierarchy lookups
  }
  Note: 'Hierarchical classification of artistic/philosophical movements (e.g., Modernism > Surrealism).'
}

Table themes {
  theme_id integer [pk, increment]
  name varchar(255) [not null]
  description text
  parent_theme_id integer [ref: > themes.theme_id] // Self-ref for hierarchy
  Indexes {
    (name, parent_theme_id) [unique, name: 'uq_themes_name_parent'] // Composite unique constraint implicitly creates an index
    parent_theme_id // Index on FK for hierarchy lookups
  }
  Note: 'Hierarchical classification of themes (e.g., Human Condition > Mortality > Death).'
}

Table formats {
  format_id integer [pk, increment]
  name varchar(100) [unique, not null]
  description text
  applies_to_work_type_id integer [ref: > work_types.work_type_id] // Optional scoping link
  Note: 'Specific forms or structures (e.g., Novel, Essay, Sonata, Etching, Documentary Film).'
  Indexes {
    name // Index on name column (unique constraint already implies one, but explicit is fine)
  }
}

Table subjects {
  subject_id integer [pk, increment]
  name varchar(255) [unique, not null]
  description text
  Note: 'Specific topics or subjects depicted or discussed (e.g., French Revolution, Quantum Mechanics, Portraiture).'
  Indexes {
    name // Index on name column
  }
}

Table keywords {
  keyword_id integer [pk, increment]
  name varchar(100) [unique, not null]
  Note: 'Less formal, specific tags or keywords (e.g., Paris, Lovecraftian, Dystopian).'
  Indexes {
    name // Index on name column
  }
}

Table attributes { // For qualitative descriptors like 'Encyclopedic'
  attribute_id integer [pk, increment]
  name varchar(100) [unique, not null]
  description text
  category varchar(50) // Optional grouping (e.g., 'Scope', 'Style', 'Structure')
  Note: 'Qualitative characteristics or stylistic attributes (e.g., Encyclopedic, Experimental, Minimalist).'
  Indexes {
    name // Index on name column
  }
}

Table series {
  series_id integer [pk, increment]
  name varchar(255) [unique, not null]
  description text
  parent_series_id integer [ref: > series.series_id] // Self-ref for hierarchy
  Note: 'Groups works belonging to a named series.'
  Indexes {
    name // Index on name column
    parent_series_id // Index on FK for hierarchy lookups
  }
}


// --- Core Entity Tables ---

Table people {
  person_id integer [pk, increment]
  first_name varchar(150)
  last_name varchar(150)
  birth_name varchar(300)
  sort_name varchar(300) [unique, not null] // e.g., 'Deleuze, Gilles' or 'Plato'
  display_name varchar(300) [not null] // e.g., 'Gilles Deleuze'
  gender varchar(50)
  birth_date date
  death_date date
  birth_country_id integer [ref: > countries.country_id]
  death_city varchar(100)
  death_country_id integer [ref: > countries.country_id]
  biography text
  profile_image_url varchar(512)
  cover_image_url varchar(512)
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`] // Use DB trigger for on update
  Note: 'Stores information about creators, contributors, subjects.'
  Indexes {
    sort_name // Index on sort_name (unique constraint already provides one)
    last_name // Index on last_name for searching
  }
}

Table works {
  work_id integer [pk, increment]
  work_type_id integer [not null, ref: > work_types.work_type_id]
  primary_title varchar(512) [not null]
  subtitle varchar(512)
  original_language_id integer [ref: > languages.language_id]
  creation_year_start integer
  creation_year_end integer
  description text
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`] // Use DB trigger for on update
  Note: 'Represents the abstract concept of a creative work.'
  Indexes {
    work_type_id
    primary_title
    creation_year_start
  }
}

Table manifestations {
  manifestation_id integer [pk, increment]
  work_id integer [not null, ref: > works.work_id]
  edition_title varchar(512) // Specific title if different from work (e.g., "Director's Cut")
  identifier varchar(255) // ISBN, ISMN, Accession#, Catalog#, DOI etc.
  identifier_type varchar(50) // 'ISBN-13', 'LoC', 'Accession #' etc.
  publisher_id integer [ref: > publishing_houses.publisher_id]
  perfume_house_id integer [ref: > perfume_houses.perfume_house_id]
  publication_date date
  language_id integer [ref: > languages.language_id]
  format_details varchar(255) // e.g., 'Hardcover', 'Oil on Canvas', 'Eau de Parfum Spray', 'FLAC'
  location varchar(255) // Museum, Library shelf, File path, URL
  specific_attributes jsonb // Stores type-specific fields (pages, medium, concentration, volume_ml, dimensions_cm, translator_id etc.)
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`] // Use DB trigger for on update
  Note: 'Represents concrete instances/editions/versions of a Work.'
  Indexes {
    work_id
    identifier
    publisher_id
    perfume_house_id
    publication_date
    language_id
    // GIN index on specific_attributes would be added in SQL/Alembic if needed
  }
}


// --- User Interaction Tables ---

Table user_interactions {
  interaction_id integer [pk, increment]
  // user_id integer [ref: > users.user_id] // Add if multi-user needed
  manifestation_id integer [unique, not null, ref: > manifestations.manifestation_id] // One interaction per manifestation
  personal_relevance smallint // CHECK (1-5) constraint recommended
  ownership_status varchar(50) // CHECK/ENUM ('Owned', 'Wishlist', 'Borrowed') recommended
  read_view_status varchar(50) // CHECK/ENUM ('To Read', 'Completed', 'DNF') recommended
  date_acquired date
  date_started date
  date_completed date
  personal_notes text
  current_rating smallint // CHECK (1-10 or 1-5) constraint recommended
  created_at timestamptz [not null, default: `now()`]
  updated_at timestamptz [not null, default: `now()`] // Use DB trigger for on update
  Note: 'Tracks personal interaction with a specific manifestation.'
  Indexes {
    manifestation_id // Unique constraint already implies one
    personal_relevance
    ownership_status
    read_view_status
    current_rating
  }
}

Table rating_history {
  rating_history_id integer [pk, increment]
  interaction_id integer [not null, ref: > user_interactions.interaction_id]
  rating smallint [not null] // CHECK (1-10 or 1-5) constraint recommended
  rated_at timestamptz [not null, default: `now()`]
  rating_notes text
  Note: 'Stores historical ratings for an interaction.'
  Indexes {
    interaction_id
    rated_at
  }
}


// --- Association Tables / Models (Handling Many-to-Many & Complex Relationships) ---

// Junction Table: People <-> Countries (Nationality)
Table person_nationalities {
  person_id integer [ref: > people.person_id, pk]
  country_id integer [ref: > countries.country_id, pk]
}

// Association Model: Works <-> People (Contribution) + Details
Table work_contributors {
  work_id integer [ref: > works.work_id, pk]
  person_id integer [ref: > people.person_id, pk]
  contribution_type_id integer [ref: > contribution_types.contribution_type_id, pk]
  contribution_details text // e.g., Role clarification 'as Mephistopheles', 'uncredited'
  Indexes {
     person_id // Index contributors by person
     contribution_type_id // Index contributors by role type
  }
}

// Association Model: Works <-> Series + Details
Table work_series {
  work_id integer [ref: > works.work_id, pk]
  series_id integer [ref: > series.series_id, pk]
  series_number numeric(8,2) // Flexible numbering (1, 1.5, 2, etc.)
  Indexes {
     series_id // Index works by series
  }
}

// Junction Table: Works <-> Genres
Table work_genres {
  work_id integer [ref: > works.work_id, pk]
  genre_id integer [ref: > genres.genre_id, pk]
  Indexes {
     genre_id // Index works by genre
  }
}

// Junction Table: Works <-> Movements
Table work_movements {
  work_id integer [ref: > works.work_id, pk]
  movement_id integer [ref: > movements.movement_id, pk]
  Indexes {
     movement_id // Index works by movement
  }
}

// Junction Table: Works <-> Themes
Table work_themes {
  work_id integer [ref: > works.work_id, pk]
  theme_id integer [ref: > themes.theme_id, pk]
  Indexes {
     theme_id // Index works by theme
  }
}

// Junction Table: Works <-> Formats
Table work_formats {
  work_id integer [ref: > works.work_id, pk]
  format_id integer [ref: > formats.format_id, pk]
  Indexes {
     format_id // Index works by format
  }
}

// Junction Table: Works <-> Subjects
Table work_subjects {
  work_id integer [ref: > works.work_id, pk]
  subject_id integer [ref: > subjects.subject_id, pk]
  Indexes {
     subject_id // Index works by subject
  }
}

// Junction Table: Works <-> Keywords
Table work_keywords {
  work_id integer [ref: > works.work_id, pk]
  keyword_id integer [ref: > keywords.keyword_id, pk]
  Indexes {
     keyword_id // Index works by keyword
  }
}

// Junction Table: Works <-> Attributes (For tags like 'Encyclopedic')
Table work_attributes {
  work_id integer [ref: > works.work_id, pk]
  attribute_id integer [ref: > attributes.attribute_id, pk]
  Indexes {
     attribute_id // Index works by attribute
  }
}

So what I want to do is prepare all my data in the excel file to be loaded into a database, but I first want to create a unique source of truth for all my information, and this is where this part of the application comes into play: I want to read all the info from the excel file, and create parquet files that have a more similar structure to what we're expecting from the database.

I already have this code:

# main.py
import logging
import sys
import time

import pandas as pd

# Use absolute imports based on the CORRECT package structure
from phantom_canon import constants, file_io, cli_display # <--- Import cli_display
from phantom_canon.processing import people_processor
# from phantom_canon.processing import books_processor # etc.

# --- Configuration ---
# Log level can be controlled here or via CLI args later
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Setup logging using RichHandler from cli_display
# Note: format="%(message)s" because RichHandler handles the rest
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(message)s",
    datefmt="[%X]", # Time format used by handler if show_time=True
    handlers=[cli_display.get_rich_logger_handler(level=LOG_LEVEL)]
)
log = logging.getLogger(__name__) # Get logger (will use Rich handler)

# --- Main Application Logic ---

def initial_excel_load() -> bool:
    """Loads data from Excel sheets and saves raw parquet checkpoints."""
    cli_display.print_sub_header("Stage 1: Initial Load from Excel")
    overall_success = True
    tasks_failed = []

    # --- Load People ---
    task_name = "Load People from Excel"
    cli_display.task_start(task_name)
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

    # --- Load Books ---
    task_name = "Load Books from Excel"
    cli_display.task_start(task_name)
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
        # Treat load failure as a warning for now, processing can continue for others
        cli_display.task_warning(f"{task_name} failed or sheet empty.")
        # tasks_failed.append(task_name) # Uncomment if load failure is critical
        # overall_success = False        # Uncomment if load failure is critical


    # --- Load Films ---
    task_name = "Load Films from Excel"
    cli_display.task_start(task_name)
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


    # --- Load Reference Tables ---
    task_name = "Load Countries Reference"
    cli_display.task_start(task_name)
    df_countries_ref = file_io.load_excel_sheet(sheet_name=constants.SHEET_COUNTRIES)
    if df_countries_ref is not None:
        cli_display.task_success(task_name, f"Loaded {len(df_countries_ref)} rows")
        cli_display.print_filename(str(constants.EXCEL_FILE))
        save_task_name = "Save Countries reference"
        cli_display.task_start(save_task_name)
        # Clean and add ID
        df_countries_ref.columns = df_countries_ref.columns.str.strip()
        if constants.COUNTRY_ID not in df_countries_ref.columns:
             df_countries_ref = df_countries_ref.reset_index().rename(columns={"index": constants.COUNTRY_ID})
             df_countries_ref[constants.COUNTRY_ID] += 1
        if file_io.save_parquet(df_countries_ref, constants.COUNTRIES_PQ):
             cli_display.task_success(save_task_name)
             cli_display.print_filename(str(constants.COUNTRIES_PQ))
        else:
             cli_display.task_failure(save_task_name)
             tasks_failed.append(save_task_name)
             overall_success = False
    else:
        cli_display.task_warning(f"{task_name} failed. Nationality processing may be incomplete.")
        # Decide if this is critical
        # tasks_failed.append(task_name)
        # overall_success = False

    # Add loading for other reference tables (Series, Publishers, etc.) similarly...

    if not overall_success:
        log.error(f"Initial Excel Load Stage completed with failures: {tasks_failed}")
    else:
        log.info("--- Initial Excel Load Stage completed successfully ---")

    return overall_success


def process_data() -> bool:
    """Loads raw data from parquet, processes it, and saves final parquet files."""
    cli_display.print_sub_header("Stage 2: Processing Data")
    overall_success = True
    tasks_failed = []

    # --- Process People ---
    process_task_name = "Process People Data"
    cli_display.task_start(process_task_name)
    df_people_raw = file_io.load_parquet(constants.PEOPLE_RAW_PQ)
    df_countries_ref = file_io.load_parquet(constants.COUNTRIES_PQ)

    if df_people_raw is not None:
        try:
            df_people_final, df_person_nationalities = people_processor.process_people(
                df_people_raw, df_countries_ref
            )

            if df_people_final is not None:
                 cli_display.task_success(process_task_name, f"Processed {len(df_people_final)} people")
                 save_task_name = "Save final People parquet"
                 cli_display.task_start(save_task_name)
                 if file_io.save_parquet(df_people_final, constants.PEOPLE_PQ):
                     cli_display.task_success(save_task_name)
                     cli_display.print_filename(str(constants.PEOPLE_PQ))
                 else:
                     cli_display.task_failure(save_task_name)
                     tasks_failed.append(save_task_name)
                     overall_success = False
            else:
                 cli_display.task_failure(process_task_name, "Processing function returned None")
                 tasks_failed.append(process_task_name)
                 overall_success = False

            if df_person_nationalities is not None:
                 save_task_name = "Save Person Nationalities parquet"
                 cli_display.task_start(save_task_name)
                 if file_io.save_parquet(df_person_nationalities, constants.PERSON_NATIONALITIES_PQ):
                      cli_display.task_success(save_task_name, f"Saved {len(df_person_nationalities)} links")
                      cli_display.print_filename(str(constants.PERSON_NATIONALITIES_PQ))
                 else:
                      cli_display.task_failure(save_task_name)
                      tasks_failed.append(save_task_name)
                      overall_success = False
            else:
                 # It's okay if this is None or empty if no nationalities were found/processed
                 cli_display.task_info("Person Nationalities processing returned None or empty DataFrame.")

        except Exception as e:
             cli_display.task_failure(process_task_name, "An exception occurred during processing")
             log.error(f"Error processing people data: {e}")
             cli_display.print_exception() # Print formatted traceback
             tasks_failed.append(process_task_name)
             overall_success = False

    else:
        cli_display.task_warning("Skipping People processing", "Raw Parquet file not found.")
        tasks_failed.append(process_task_name + " (skipped)")
        # Decide if skipping is a failure
        # overall_success = False

    # --- Process Books ---
    process_task_name = "Process Books Data"
    cli_display.task_start(process_task_name + " (Placeholder)")
    df_books_raw = file_io.load_parquet(constants.BOOKS_RAW_PQ)
    if df_books_raw is not None:
        # Placeholder - Add calls to books_processor here
        time.sleep(0.5) # Simulate work
        cli_display.task_warning(process_task_name, "Processing logic not yet implemented.")
    else:
         cli_display.task_warning(f"Skipping {process_task_name}", "Raw Parquet file not found.")

    # --- Process Films ---
    process_task_name = "Process Films Data"
    cli_display.task_start(process_task_name + " (Placeholder)")
    df_films_raw = file_io.load_parquet(constants.FILMS_RAW_PQ)
    if df_films_raw is not None:
        # Placeholder - Add calls to films_processor here
        time.sleep(0.5) # Simulate work
        cli_display.task_warning(process_task_name, "Processing logic not yet implemented.")
    else:
         cli_display.task_warning(f"Skipping {process_task_name}", "Raw Parquet file not found.")


    if not overall_success:
        log.error(f"Data Processing Stage completed with failures: {tasks_failed}")
    else:
        log.info("--- Data Processing Stage completed successfully ---")

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
        # Catch unexpected errors in the main flow
        log.critical(f"Critical error in main execution flow: {e}")
        cli_display.print_exception() # Print formatted traceback via rich
        overall_success = False # Ensure failure state
    finally:
        # Always print summary
        duration = time.time() - start_time
        cli_display.print_summary(duration, overall_success)
        sys.exit(0 if overall_success else 1) # Exit with appropriate code

if __name__ == "__main__":
    main()
	
# pyproject.toml

[tool.poetry]
name = "phantom-canon"
version = "0.1.0"
description = "Processing and enrichment for the Phantom knowledge base"
authors = ["Pablo Aguirre <main@pabloagn.com>"]
readme = "README.md"
packages = [{include = "phantom_canon"}]

[tool.poetry.dependencies]
python = "^3.11"
pandas = "^2.2.3"
openpyxl = "^3.1.5"
pyarrow = "^19.0.1"
rich = "^14.0.0"

[tool.poetry.group.dev.dependencies]
jupyter = "^1.1.1"
black = "^25.1.0"
isort = "^6.0.1"
ruff = "^0.1.0"
mypy = "^1.0.0"

[tool.ruff]
line-length = 88
select = ["E", "W", "F", "I", "UP"]
ignore = []

[tool.ruff.isort]
known-first-party = ["phantom_canon"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

# phantom_canon/processing/people_processor.py
import logging
import re
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Use absolute imports based on the CORRECT package structure
from phantom_canon import constants # <--- CORRECTED Import

log = logging.getLogger(__name__)

# --- Helper Functions (_parse_year, _parse_full_date) ---
def _parse_year(year_str: Optional[str]) -> Tuple[Optional[int], Optional[str]]:
    """Parses a year string, handling integers, 'circa', ranges, centuries."""
    if pd.isna(year_str) or not isinstance(year_str, str) or year_str.strip() == "":
        return None, None
    year_str = year_str.strip()
    qualifier = None
    year_int = None
    if year_str.lower().startswith("c.") or year_str.lower().startswith("circa"):
        qualifier = "circa"
        year_str = re.sub(r"^[Cc](irca|\.)\s*", "", year_str).strip()
    range_match = re.match(r"^(\d{1,4})\s*-\s*(\d{1,4})$", year_str)
    if range_match:
        qualifier = qualifier or "range"
        try: year_int = int(range_match.group(1))
        except ValueError: pass
    century_match = re.match(r"^(?:(\d{1,2})(?:st|nd|rd|th))?\s*[Cc]entury(?:\s*(BCE|BC|CE|AD))?$", year_str, re.IGNORECASE)
    if century_match:
        qualifier = qualifier or "century"
        try:
             century_num = int(century_match.group(1))
             year_int = (century_num * 100) - 50 # Mid-century estimate
        except (ValueError, TypeError): pass
    if year_int is None:
        try: year_int = int(float(year_str))
        except (ValueError, TypeError): log.debug(f"Could not parse year '{year_str}' to int.")
    if year_int is not None and (year_int < -4000 or year_int > 2100):
        log.debug(f"Parsed year {year_int} from '{year_str}' out of range.")
        year_int = None
    return year_int, qualifier

def _parse_full_date(d: Optional[str], m: Optional[str], y: Optional[str]) -> Tuple[Optional[pd.Timestamp], Optional[int], Optional[str], Optional[str]]:
    """Attempts to parse day, month, year into a Timestamp and extracts year/qualifier."""
    original_parts = [str(p) for p in [d, m, y] if pd.notna(p) and str(p).strip() != ""]
    original_str = " / ".join(original_parts) if original_parts else None
    year_int, qualifier = _parse_year(y)
    timestamp = pd.NaT
    if pd.notna(d) and pd.notna(m) and year_int is not None:
         try:
             date_str = f"{int(year_int)}-{int(m):02d}-{int(d):02d}"
             timestamp = pd.to_datetime(date_str, errors='coerce')
         except (ValueError, TypeError): timestamp = pd.NaT
    if pd.isna(timestamp) and year_int is not None:
         try: timestamp = pd.to_datetime(f"{year_int}-01-01", errors='coerce')
         except ValueError: timestamp = pd.NaT
    return timestamp, year_int, original_str, qualifier

# --- Main Processing Function ---

def process_people(
    df_raw: pd.DataFrame, df_countries: Optional[pd.DataFrame]
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """Transforms raw people data to the target schema."""
    if df_raw is None:
        log.error("Received None instead of a DataFrame for raw people data.")
        return None, None
    if df_countries is None:
        log.warning("Countries DataFrame is None. Cannot process nationalities.")
        # Decide if this is fatal or just skip nationality processing
        # return None, None # Uncomment if countries are essential

    log.info(f"Processing {len(df_raw)} raw people entries...")
    df = df_raw.copy()

    # 1. Generate Unique Person ID
    df = df.reset_index().rename(columns={"index": constants.PERSON_ID})
    df[constants.PERSON_ID] = df[constants.PERSON_ID] + 1

    # 2. Parse Names
    df[constants.PERSON_FIRST_NAME] = df[constants.EXCEL_PEOPLE_NAME].fillna('').astype(str)
    df[constants.PERSON_LAST_NAME] = df[constants.EXCEL_PEOPLE_SURNAME].fillna('').astype(str)
    df[constants.PERSON_BIRTH_NAME] = df[constants.EXCEL_PEOPLE_REAL_NAME].fillna('').astype(str)
    df[constants.PERSON_DISPLAY_NAME] = df.apply(
        lambda r: f"{r[constants.PERSON_FIRST_NAME]} {r[constants.PERSON_LAST_NAME]}".strip()
        if r[constants.PERSON_LAST_NAME] else r[constants.PERSON_FIRST_NAME], axis=1
    )
    df[constants.PERSON_SORT_NAME] = df.apply(
        lambda r: f"{r[constants.PERSON_LAST_NAME]}, {r[constants.PERSON_FIRST_NAME]}".strip(', ')
        if r[constants.PERSON_LAST_NAME] else r[constants.PERSON_FIRST_NAME], axis=1
    )

    # 3. Parse Dates
    birth_info = df.apply(lambda r: _parse_full_date(r.get(constants.EXCEL_PEOPLE_BIRTH_DAY), r.get(constants.EXCEL_PEOPLE_BIRTH_MONTH), r.get(constants.EXCEL_PEOPLE_BIRTH_YEAR)), axis=1, result_type='expand')
    df[[constants.PERSON_BIRTH_DATE, constants.PERSON_BIRTH_YEAR, constants.PERSON_BIRTH_DATE_ORIGINAL, constants.PERSON_BIRTH_DATE_QUALIFIER]] = birth_info
    death_info = df.apply(lambda r: _parse_full_date(r.get(constants.EXCEL_PEOPLE_DEATH_DAY), r.get(constants.EXCEL_PEOPLE_DEATH_MONTH), r.get(constants.EXCEL_PEOPLE_DEATH_YEAR)), axis=1, result_type='expand')
    df[[constants.PERSON_DEATH_DATE, constants.PERSON_DEATH_YEAR, constants.PERSON_DEATH_DATE_ORIGINAL, constants.PERSON_DEATH_DATE_QUALIFIER]] = death_info

    # Ensure correct final dtypes
    df[constants.PERSON_BIRTH_DATE] = pd.to_datetime(df[constants.PERSON_BIRTH_DATE], errors='coerce')
    df[constants.PERSON_DEATH_DATE] = pd.to_datetime(df[constants.PERSON_DEATH_DATE], errors='coerce')
    df[constants.PERSON_BIRTH_YEAR] = pd.to_numeric(df[constants.PERSON_BIRTH_YEAR], errors='coerce').astype('Int64')
    df[constants.PERSON_DEATH_YEAR] = pd.to_numeric(df[constants.PERSON_DEATH_YEAR], errors='coerce').astype('Int64')
    df[constants.PERSON_BIRTH_DATE_ORIGINAL] = df[constants.PERSON_BIRTH_DATE_ORIGINAL].astype("string")
    df[constants.PERSON_DEATH_DATE_ORIGINAL] = df[constants.PERSON_DEATH_DATE_ORIGINAL].astype("string")
    df[constants.PERSON_BIRTH_DATE_QUALIFIER] = df[constants.PERSON_BIRTH_DATE_QUALIFIER].astype("string")
    df[constants.PERSON_DEATH_DATE_QUALIFIER] = df[constants.PERSON_DEATH_DATE_QUALIFIER].astype("string")


    # 4. Clean Gender
    df[constants.PERSON_GENDER] = df[constants.EXCEL_PEOPLE_GENDER].fillna('Unknown').astype(str).str.strip().str.capitalize()

    # 5. Process Nationalities (Junction Table)
    nationalities_records = []
    country_lookup = {}
    if df_countries is not None and constants.EXCEL_COUNTRY_NAME in df_countries.columns and constants.COUNTRY_ID in df_countries.columns:
        # Build lookup cache: lowercase name -> ID
        country_lookup = df_countries.set_index(df_countries[constants.EXCEL_COUNTRY_NAME].str.lower().str.strip())[constants.COUNTRY_ID].to_dict()
        log.info(f"Created country lookup with {len(country_lookup)} entries.")
    else:
        log.warning("Cannot create country lookup map. Country data missing or incomplete.")

    if country_lookup: # Only proceed if lookup exists
        for _, row in df.iterrows():
            person_id = row[constants.PERSON_ID]
            nationality_str = row.get(constants.EXCEL_PEOPLE_NATIONALITY)
            if pd.notna(nationality_str) and isinstance(nationality_str, str):
                nationalities = [n.strip().lower() for n in nationality_str.split(constants.DEFAULT_MULTI_VALUE_SEP) if n.strip()]
                for nat_name_lower in nationalities:
                    country_id = country_lookup.get(nat_name_lower)
                    if country_id:
                        nationalities_records.append({
                            constants.NATIONALITY_PERSON_ID: person_id,
                            constants.NATIONALITY_COUNTRY_ID: country_id
                        })
                    else:
                        # Handle non-contemporary or ambiguous? Fuzzy match? Log?
                        log.warning(f"Could not map nationality '{nat_name_lower}' to a country ID for person_id {person_id}.")

    df_person_nationalities = pd.DataFrame(nationalities_records).drop_duplicates()
    log.info(f"Created {len(df_person_nationalities)} person-nationality links.")

    # 6. Select and Order Final Columns for 'people' table
    final_people_cols = [
        constants.PERSON_ID, constants.PERSON_FIRST_NAME, constants.PERSON_LAST_NAME,
        constants.PERSON_SORT_NAME, constants.PERSON_DISPLAY_NAME, constants.PERSON_BIRTH_NAME,
        constants.PERSON_GENDER, constants.PERSON_BIRTH_DATE, constants.PERSON_BIRTH_YEAR,
        constants.PERSON_BIRTH_DATE_ORIGINAL, constants.PERSON_BIRTH_DATE_QUALIFIER,
        constants.PERSON_DEATH_DATE, constants.PERSON_DEATH_YEAR,
        constants.PERSON_DEATH_DATE_ORIGINAL, constants.PERSON_DEATH_DATE_QUALIFIER
        # Add other target columns as they are processed (e.g., birth/death country IDs)
    ]
    # Ensure all columns exist, adding missing ones as NA if needed
    for col in final_people_cols:
        if col not in df.columns:
            df[col] = pd.NA # Or appropriate default

    df_people_final = df[final_people_cols]
    log.info(f"Final people DataFrame created with {len(df_people_final)} rows and columns: {df_people_final.columns.tolist()}")

    return df_people_final, df_person_nationalities
	
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

      
# phantom_canon/constants.py
import pathlib
from typing import Dict, List, Set

# --- Base Project Directory ---
# Assumes constants.py is in phantom_canon/ subdirectory
BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent

# --- Input Files ---
DATA_DIR: pathlib.Path = BASE_DIR / "data"
# Verify filename extension (.xlsx or .xlsm)
EXCEL_FILE: pathlib.Path = DATA_DIR / "knowledge_base.xlsm"

# --- Output/Persistent Store ---
PARQUET_DIR: pathlib.Path = DATA_DIR / "parquet_store"
PARQUET_DIR.mkdir(parents=True, exist_ok=True)

# --- Excel Sheet Names (CRITICAL: Verify these names) ---
SHEET_PEOPLE: str = "People"
SHEET_BOOKS: str = "Books"
SHEET_FILMS: str = "Films"
SHEET_COUNTRIES: str = "Countries"
SHEET_LANGUAGES: str = "Languages"
SHEET_BOOK_SERIES: str = "Series"
SHEET_PUBLISHERS: str = "Publishers"
SHEET_ART_TYPES: str = "ArtTypes"

# --- Excel Table Names (Defined in Excel Name Manager - Verify) ---
TABLE_PEOPLE: str = "Table_People"
TABLE_BOOKS: str = "Table_Books"
TABLE_FILMS: str = "Table_Films"
TABLE_COUNTRIES: str = "Table_Countries"
TABLE_LANGUAGES: str = "Table_Languages"
TABLE_BOOK_SERIES: str = "Table_Book_Series"
TABLE_PUBLISHING_HOUSES: str = "Table_Publishing_Houses"
TABLE_ART_TYPES: str = "Table_Art_Types"

# --- Target Parquet Filenames (Final Processed Data) ---
PEOPLE_PQ: pathlib.Path = PARQUET_DIR / "people.parquet"
WORKS_PQ: pathlib.Path = PARQUET_DIR / "works.parquet"
MANIFESTATIONS_PQ: pathlib.Path = PARQUET_DIR / "manifestations.parquet"
COUNTRIES_PQ: pathlib.Path = PARQUET_DIR / "countries.parquet"
LANGUAGES_PQ: pathlib.Path = PARQUET_DIR / "languages.parquet"
PUBLISHING_HOUSES_PQ: pathlib.Path = PARQUET_DIR / "publishing_houses.parquet"
SERIES_PQ: pathlib.Path = PARQUET_DIR / "series.parquet"
WORK_CONTRIBUTORS_PQ: pathlib.Path = PARQUET_DIR / "work_contributors.parquet"
PERSON_NATIONALITIES_PQ: pathlib.Path = PARQUET_DIR / "person_nationalities.parquet"
WORK_SERIES_PQ: pathlib.Path = PARQUET_DIR / "work_series.parquet"
USER_INTERACTIONS_PQ: pathlib.Path = PARQUET_DIR / "user_interactions.parquet"

# --- Temporary Raw Parquet Filenames (Checkpoints) ---
PEOPLE_RAW_PQ: pathlib.Path = PARQUET_DIR / "people_raw_temp.parquet"
BOOKS_RAW_PQ: pathlib.Path = PARQUET_DIR / "books_raw_temp.parquet"
FILMS_RAW_PQ: pathlib.Path = PARQUET_DIR / "films_raw_temp.parquet"
COUNTRIES_RAW_PQ: pathlib.Path = PARQUET_DIR / "countries_raw_temp.parquet"

# === Column Definitions ===

# --- People Columns ---
EXCEL_PEOPLE_HASH_ID: str = "Hash_ID"
EXCEL_PEOPLE_NAME: str = "Name"
EXCEL_PEOPLE_SURNAME: str = "Surname"
EXCEL_PEOPLE_REAL_NAME: str = "Real Name"
EXCEL_PEOPLE_TYPE: str = "Type"
EXCEL_PEOPLE_GENDER: str = "Gender"
EXCEL_PEOPLE_NATIONALITY: str = "Nationality"
EXCEL_PEOPLE_BIRTH_DAY: str = "Birth_Date_Day"
EXCEL_PEOPLE_BIRTH_MONTH: str = "Birth_Date_Month"
EXCEL_PEOPLE_BIRTH_YEAR: str = "Birth_Date_Year"
EXCEL_PEOPLE_BIRTH_RANGE: str = "Birth_Date_Year_IsRange"
EXCEL_PEOPLE_DEATH_DAY: str = "Death_Date_Day"
EXCEL_PEOPLE_DEATH_MONTH: str = "Death_Date_Month"
EXCEL_PEOPLE_DEATH_YEAR: str = "Death_Date_Year"
EXCEL_PEOPLE_DEATH_RANGE: str = "Death_Date_Year_IsRange"

PEOPLE_EXCEL_COLS_NEEDED: List[str] = [
    EXCEL_PEOPLE_HASH_ID, EXCEL_PEOPLE_NAME, EXCEL_PEOPLE_SURNAME,
    EXCEL_PEOPLE_REAL_NAME, EXCEL_PEOPLE_TYPE, EXCEL_PEOPLE_GENDER,
    EXCEL_PEOPLE_NATIONALITY, EXCEL_PEOPLE_BIRTH_DAY, EXCEL_PEOPLE_BIRTH_MONTH,
    EXCEL_PEOPLE_BIRTH_YEAR, EXCEL_PEOPLE_BIRTH_RANGE, EXCEL_PEOPLE_DEATH_DAY,
    EXCEL_PEOPLE_DEATH_MONTH, EXCEL_PEOPLE_DEATH_YEAR, EXCEL_PEOPLE_DEATH_RANGE
]
PEOPLE_RAW_SAVE_STR_COLS: Set[str] = {
    EXCEL_PEOPLE_BIRTH_YEAR, EXCEL_PEOPLE_DEATH_YEAR,
    EXCEL_PEOPLE_BIRTH_DAY, EXCEL_PEOPLE_BIRTH_MONTH,
    EXCEL_PEOPLE_DEATH_DAY, EXCEL_PEOPLE_DEATH_MONTH,
}

# Target 'people' parquet/DB columns
PERSON_ID: str = "person_id"
PERSON_FIRST_NAME: str = "first_name"
PERSON_LAST_NAME: str = "last_name"
PERSON_BIRTH_NAME: str = "birth_name"
PERSON_SORT_NAME: str = "sort_name"
PERSON_DISPLAY_NAME: str = "display_name"
PERSON_GENDER: str = "gender"
PERSON_BIRTH_DATE: str = "birth_date"
PERSON_BIRTH_YEAR: str = "birth_year"
PERSON_BIRTH_DATE_ORIGINAL: str = "birth_date_original"
PERSON_BIRTH_DATE_QUALIFIER: str = "birth_date_qualifier"
PERSON_DEATH_DATE: str = "death_date"
PERSON_DEATH_YEAR: str = "death_year"
PERSON_DEATH_DATE_ORIGINAL: str = "death_date_original"
PERSON_DEATH_DATE_QUALIFIER: str = "death_date_qualifier"

# Target 'person_nationalities' parquet/DB columns
NATIONALITY_PERSON_ID: str = "person_id"
NATIONALITY_COUNTRY_ID: str = "country_id"

# --- Books Columns --- (Verify and define needed/str cols)
EXCEL_BOOKS_TITLE: str = "Title"
EXCEL_BOOKS_AUTHOR: str = "Author"
BOOKS_EXCEL_COLS_NEEDED: List[str] = [
    "Title", "Author", "Series", "Series_Number", "Published_Date", "Edition",
    "Publisher", "Published_Title", "Published_Language", "Page_Count",
    "Rating", "Read", "Started_Date", "Finished_Date",
    "Hardcover_ID", "Goodreads_URL" # Adjust as per your Excel
]
BOOKS_RAW_SAVE_STR_COLS: Set[str] = {EXCEL_BOOKS_TITLE, "Published_Date", "Page_Count"} # Add others prone to errors

# --- Films Columns --- (Verify and define needed/str cols)
EXCEL_FILMS_TITLE: str = "Title"
FILMS_EXCEL_COLS_NEEDED: List[str] = ["Title", "Director", "Year"]
FILMS_RAW_SAVE_STR_COLS: Set[str] = {EXCEL_FILMS_TITLE, "Year"}

# --- Countries Columns ---
EXCEL_COUNTRY_NAME: str = "Country_Name"
EXCEL_COUNTRY_ALPHA2: str = "Two_Letter_Country_Code"
EXCEL_COUNTRY_ALPHA3: str = "Three_Letter_Country_Code"
COUNTRY_ID: str = "country_id"

# --- General Processing ---
DEFAULT_MULTI_VALUE_SEP: str = ";"

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
		
# .gitignore file for phantom-canon

# Resources
resources/

# Python
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
.venv/
venv/
ENV/
env/
virtualenv/
*.egg-info/
.installed.cfg
*.egg

# Poetry
dist/
build/
.env

# VS Code
.vscode/

# Data Files (Optional)
# data/parquet_store/*
# !data/parquet_store/.gitkeep # Keep the directory structure

# OS specific
.DS_Store
Thumbs.db

You need to help me finish this application so I can execute it (main.py) and it loads all the excel tables into parquet tables with the appropriate data type, col names, and everything required for us to quickly query in Python and later on load to our PostgreSQL database.

based on this info, what questions do you have?

# FAQ
Based on the information provided, here are my clarifying questions to ensure I understand the requirements fully before suggesting the next steps for implementation:

1.  **Excel Data Structure & Content:**
    *   **Column Names:** Can you confirm the *exact* column names present in the `Books`, `Films`, `Languages`, `Series` (assuming this is `SHEET_BOOK_SERIES`), `Publishers`, and `ArtTypes` sheets within `knowledge_base.xlsm`? Do the `EXCEL_*` constants in `constants.py` accurately reflect these for the sheets they cover?
    *   **Multi-Value Fields:** In the `Books` and `Films` sheets (and potentially others), how are multiple values represented in columns like Authors, Directors, Genres, Themes, Keywords, etc.? Is it consistently a semicolon (`;`) separated string, or are there variations? (Consistent with Semicolon)
    *   **Data for Taxonomy/Reference Tables:** Where does the source data for tables like `genres`, `movements`, `themes`, `formats`, `subjects`, `keywords`, `attributes`, `work_types`, and `contribution_types` come from? Are they:
        *   Separate sheets in the Excel file? (If so, what are their names and columns?)
        *   Derived from specific columns within the `Books` or `Films` sheets? (e.g., a "Genre" column in the Books sheet)
        *   Expected to be manually created or populated later? YES. Leave this for now.
    *   **Hierarchical Data:** For hierarchical tables like `genres`, `movements`, `themes`, and `series`, how is the parent-child relationship represented in the source Excel data (if at all)? Wide representation. Check schemas at the end of the message.

2.  **Schema Mapping & Entity Representation:**
    *   **Work vs. Manifestation:** Does a single row in the `Books` sheet represent an abstract `Work` (the concept of the book) or a specific `Manifestation` (a particular edition/printing)? Similarly for `Films`? Books table, films table, etc, represent only one unique author_work entry. The manifestations are the "editions".
    *   **Linking Works and Manifestations:** If a row represents a manifestation, how do we identify and group manifestations that belong to the same underlying `Work`? Is there a common identifier or combination of fields (e.g., Title + Author/Director)? We need to create these mappings with IDs. for now don't focus on the manifestations table, since I don't yet have the complete editions data.
    *   **Manifestation Identifiers:** Do the `Books`/`Films` sheets contain columns for identifiers like ISBN, ISMN, DOIs, Catalogue Numbers, etc., that should map to `manifestations.identifier`? Answered above.
    *   **`specific_attributes` (JSONB):** Which columns from the `Books`, `Films`, (and potentially other source sheets like art) should be mapped into the `manifestations.specific_attributes` JSONB field? (e.g., `Page_Count`, `Medium`, `Dimensions`, `Translator`, `Film Runtime`, etc.) For now don't focus on the manifestations.

3.  **Processing Logic & IDs:**
    *   **Work/Manifestation IDs:** How should `work_id` and `manifestation_id` be generated? Similar to `person_id` (simple increment), or should we attempt deduplication based on certain fields? This is a crucial point. We need to create unique IDs for the works table. These IDs need to be unique per work entry.
    *   **Linking Contributors:** How are contributors (Authors, Directors, etc.) listed in the `Books`/`Films` sheets? Is it by name? Do these names need to be matched against the processed `people` table to get the `person_id` for the `work_contributors` table? How will the `contribution_type_id` be determined (e.g., based on an Excel column or inferred)? Right now we have for example books table with the title, and author(s) separated by semicolons. We also have on the films table, Title, Director (a director is a type of contributor). So we need to somehow map this. Think of how. The Author columnn in books is the writer(s), the films table contains Director which can be one or more.
    *   **Reference Table IDs:** Do the reference sheets (`Countries`, `Languages`, `Publishers`, `Series`, etc.) in Excel already contain unique IDs, or should the script generate them (like the current tentative approach for `Countries`)? Every table we add must be populated with a unique ID. Currently we have Hash_IDs for some tables, but these were created just to deduplicate the tables. We need to find a way to build a robust ID system for our tables.

4.  **Priorities:**
    *   Which data entity (Books, Films, Languages, Publishers, Genres, etc.) would you like to focus on implementing the processing logic for next after `People`? Let us focus right now on People, Books and Films, and let us get that one straight. Afterwards we can move on to next types.

Answering these questions will help clarify the source data's structure and the desired transformations, allowing me to provide more specific guidance on completing the `*_processor.py` modules and refining the `main.py` orchestration.

List of current Excel workbook schema, containing sheet names, tables and cols:

Sheet,Table,Column
Occult_Library,Table_Occult_Library,Entry_Number
Occult_Library,Table_Occult_Library,Category_01
Occult_Library,Table_Occult_Library,Category_01_Number
Occult_Library,Table_Occult_Library,Category_02
Occult_Library,Table_Occult_Library,Category_02_Number
Occult_Library,Table_Occult_Library,Title
Occult_Library,Table_Occult_Library,Author
Occult_Library,Table_Occult_Library,Edition/Translation
Occult_Library,Table_Occult_Library,Edition_Language
Occult_Library,Table_Occult_Library,Original_Language
Occult_Library,Table_Occult_Library,Type
Occult_Library,Table_Occult_Library,Description
Occult_Library,Table_Occult_Library,Notes
People,Table_People,Hash_ID
People,Table_People,Name
People,Table_People,Surname
People,Table_People,Real Name
People,Table_People,Type
People,Table_People,Gender
People,Table_People,Nationality
People,Table_People,Birth_Date_Day
People,Table_People,Birth_Date_Month
People,Table_People,Birth_Date_Year
People,Table_People,Birth_Date_Year_Gregorian
People,Table_People,Birth_Date_Year_IsRange
People,Table_People,Death_Date_Day
People,Table_People,Death_Date_Month
People,Table_People,Death_Date_Year
People,Table_People,Death_Date_Year_Gregorian
People,Table_People,Death_Date_Year_IsRange
People,Table_People,Complete Name (Name Surname)
People,Table_People,Complete Name (Surname Name)
People,Table_People,Duplicated_Entry
People,Table_People,Has_Image [Y/N]
Calendars_Gregorian,Table_Calendars_Gregorian,Class
Calendars_Gregorian,Table_Calendars_Gregorian,Description
Books,Table_Books,Hash_ID
Books,Table_Books,Duplicated_Entry
Books,Table_Books,Title
Books,Table_Books,Author
Books,Table_Books,Series
Books,Table_Books,Series_Number
Books,Table_Books,Published_Date
Books,Table_Books,Edition
Books,Table_Books,Publisher
Books,Table_Books,Published_Title
Books,Table_Books,Published_Language
Books,Table_Books,Page_Count
Books,Table_Books,Description_GenAI
Books,Table_Books,Recommended_By
Books,Table_Books,Priority
Books,Table_Books,Rating
Books,Table_Books,Read
Books,Table_Books,Started_Date
Books,Table_Books,Finished_Date
Books,Table_Books,Library_Physical_MEX
Books,Table_Books,Library_Physical_EUR
Books,Table_Books,Library_Digital_Main
Books,Table_Books,Library_Mobile_Kindle
Books,Table_Books,Library_Mobile_iPad
Books,Table_Books,Library_Mobile_iPhone
Books,Table_Books,Goodreads_Path
Books,Table_Books,Hardcover_ID
Books,Table_Books,Hardcover_Path
Books,Table_Books,Cover_RAW
Books,Table_Books,Cover_FTD
Books,Table_Books,Published_Date_Decade
Books,Table_Books,Published_Date_Century
Books,Table_Books,Book_Type
Books,Table_Books,Temporary Tags
Books,Table_Books,Tradition
Books,Table_Books,Notes
Books,Table_Books,Composite_Work_Author
Books,Table_Books,Composite_Author_Work
Books,Table_Books,Composite_Work_Author_Clean
Books,Table_Books,Goodreads_URL
Books,Table_Books,Hardcover_URL
Films,Table_Films,Hash_ID
Films,Table_Films,Duplicated_Entry
Films,Table_Films,Title
Films,Table_Films,Director
Films,Table_Films,Composite_Work_Author
Films,Table_Films,Composite_Author_Work
Films,Table_Films,Year
Films,Table_Films,Decade
Films,Table_Films,Century
Films,Table_Films,Country
URLs,Table_URLs,Concept
URLs,Table_URLs,URL
Months,Table_Months,Month_Number
Months,Table_Months,Month_Name_Short
Months,Table_Months,Month_Name_Long
Book_Editions,Table_Book_Editions,Hash_ID
Book_Editions,Table_Book_Editions,Hash_ID_Books
Book_Editions,Table_Book_Editions,Title
Book_Editions,Table_Book_Editions,Author
Book_Editions,Table_Book_Editions,Edition
Book_Editions,Table_Book_Editions,Publisher
Book_Editions,Table_Book_Editions,Edition_Title
Book_Editions,Table_Book_Editions,Published_Title
Book_Editions,Table_Book_Editions,Published_Language
Book_Editions,Table_Book_Editions,Published_Date
Book_Editions,Table_Book_Editions,ISBN13
Book_Series,Table_Book_Series,Title
Book_Series,Table_Book_Series,Original Title
Book_Series,Table_Book_Series,Author
Book_Series,Table_Book_Series,Composite_Work_Author
Book_Series,Table_Book_Series,Composite_Author_Work
Book_Series,Table_Book_Series,Duplicated_Entry
Art_Types,Table_Art_Types,Book_Type
Art_Types,Table_Art_Types,Description
Art_Types,Table_Art_Types,Applicable_Work_Type(s)
Art_Types,Table_Art_Types,Duplicated_Entry
Book_Categories,Table_Book_Categories,Category_1
Book_Categories,Table_Book_Categories,Category_2
Book_Categories,Table_Book_Categories,Category_3
Book_Categories,Table_Book_Categories,Notes_Scope_Example
Literary_Movements,Table_Literary_Movements,Level 1 (Era/Broad School)
Literary_Movements,Table_Literary_Movements,Level 2 (Movement)
Literary_Movements,Table_Literary_Movements,Level 3 (Sub-movement/Related)
Literary_Movements,Table_Literary_Movements,Notes / Scope Example
Literary_Movements,Table_Literary_Movements,Duplicated_Entry
Themes,Table_Themes,Category
Themes,Table_Themes,Subcategory
Themes,Table_Themes,Theme
Subjects,Table27,Name
Subjects,Table27,Description (Optional)
Keywords,Table28,Name
Publisher_Specialties,Table29,Name
Paintings,Table_Paintings,Hash_ID
Paintings,Table_Paintings,Title
Paintings,Table_Paintings,Author
Paintings,Table_Paintings,Composite_Work_Author
Paintings,Table_Paintings,Duplicated_Entry
Paintings,Table_Paintings,Art_Movement
Paintings,Table_Paintings,Orientation
Paintings,Table_Paintings,Century
Attributes,Table_Attributes,Name
Attributes,Table_Attributes,Description (Optional)
Attributes,Table_Attributes,Category (Optional)
Attributes,Table_Attributes,Duplicated_Entry
Work_Types,Table_Work_Types,Name
Work_Types,Table_Work_Types,Description
Contribution_Types,Table_Contribution_types,Name
Contribution_Types,Table_Contribution_types,Description
Contribution_Types,Table_Contribution_types,Examples of Use
Validation_Fields,Table_Score_0_5_Halves,Score
Validation_Fields,Table_Check,Check
Validation_Fields,Centuries_Table,Centuries
Validation_Fields,Table_Score_0_5_Fulls,Score
Art_Movements,Art_Movements_Table,Art_Movements
Art_Movements,Art_Movements_Table,Duplicate_Entry
Languages,Table_Languages,Hash_ID
Languages,Table_Languages,Language
Languages,Table_Languages,ISO_639-1
Languages,Table_Languages,ISO_639-1_Is_Duplicate
Languages,Table_Languages,ISO_639-2
Languages,Table_Languages,ISO_639-2_Is_Duplicate
Languages,Table_Languages,ISO_639-3
Languages,Table_Languages,ISO_639-3_Is_Duplicate
Publishing_Houses,Table_Publishing_Houses,Publishing_House
Publishing_Houses,Table_Publishing_Houses,Country
Publishing_Houses,Table_Publishing_Houses,Duplicated_Entry
Publishing_Houses,Table_Publishing_Houses,Specialties
Perfume_Houses,Table19,Name
Perfume_Houses,Table19,Country
Perfume_Houses,Table19,Duplicated_Entry
Countries_Continents,Table_Countries,Continent_Name
Countries_Continents,Table_Countries,Continent_Code
Countries_Continents,Table_Countries,Country_Name
Countries_Continents,Table_Countries,Two_Letter_Country_Code
Countries_Continents,Table_Countries,Three_Letter_Country_Code
Countries_Continents,Table_Countries,Country_Number
Hash_ID_Acronyms,Table18,Field
Hash_ID_Acronyms,Table18,Acronym


Questions?