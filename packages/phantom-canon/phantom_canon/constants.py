# phantom_canon/constants.py
import pathlib
from typing import Dict, List, Set

# --- Base Project Directory ---
BASE_DIR: pathlib.Path = pathlib.Path(__file__).resolve().parent.parent

# --- Input Files ---
DATA_DIR: pathlib.Path = BASE_DIR / "data"
EXCEL_FILE: pathlib.Path = DATA_DIR / "knowledge_base.xlsx"

# --- Output/Persistent Store ---
PARQUET_DIR: pathlib.Path = DATA_DIR / "parquet_store"
PARQUET_DIR.mkdir(parents=True, exist_ok=True)

# --- Excel Sheet Names (CRITICAL: Verify these names) ---
SHEET_PEOPLE: str = "People"
SHEET_BOOKS: str = "Books"
SHEET_FILMS: str = "Films"
SHEET_COUNTRIES: str = "Countries_Continents" # Updated based on schema CSV
SHEET_LANGUAGES: str = "Languages"           # Updated based on schema CSV
SHEET_BOOK_SERIES: str = "Book_Series"       # Updated based on schema CSV
SHEET_PUBLISHERS: str = "Publishing_Houses" # Updated based on schema CSV
SHEET_WORK_TYPES: str = "Work_Types"         # Updated based on schema CSV
SHEET_CONTRIBUTION_TYPES: str = "Contribution_Types" # Updated based on schema CSV
SHEET_ART_TYPES: str = "ArtTypes" # Keep original if used elsewhere

# --- Excel Table Names (Defined in Excel Name Manager - Verify) ---
TABLE_PEOPLE: str = "Table_People"
TABLE_BOOKS: str = "Table_Books"
TABLE_FILMS: str = "Table_Films"
TABLE_COUNTRIES: str = "Table_Countries"
TABLE_LANGUAGES: str = "Table_Languages"
TABLE_BOOK_SERIES: str = "Table_Book_Series"
TABLE_PUBLISHING_HOUSES: str = "Table_Publishing_Houses"
TABLE_WORK_TYPES: str = "Table_Work_Types"
TABLE_CONTRIBUTION_TYPES: str = "Table_Contribution_types"
TABLE_ART_TYPES: str = "Table_Art_Types" # Keep original if used elsewhere

# --- Target Parquet Filenames (Final Processed Data) ---
PEOPLE_PQ: pathlib.Path = PARQUET_DIR / "people.parquet"
WORKS_PQ: pathlib.Path = PARQUET_DIR / "works.parquet"
MANIFESTATIONS_PQ: pathlib.Path = PARQUET_DIR / "manifestations.parquet" # Placeholder
COUNTRIES_PQ: pathlib.Path = PARQUET_DIR / "countries.parquet"
LANGUAGES_PQ: pathlib.Path = PARQUET_DIR / "languages.parquet"
PUBLISHING_HOUSES_PQ: pathlib.Path = PARQUET_DIR / "publishing_houses.parquet" # Placeholder
SERIES_PQ: pathlib.Path = PARQUET_DIR / "series.parquet" # Placeholder
WORK_TYPES_PQ: pathlib.Path = PARQUET_DIR / "work_types.parquet"
CONTRIBUTION_TYPES_PQ: pathlib.Path = PARQUET_DIR / "contribution_types.parquet"
WORK_CONTRIBUTORS_PQ: pathlib.Path = PARQUET_DIR / "work_contributors.parquet"
PERSON_NATIONALITIES_PQ: pathlib.Path = PARQUET_DIR / "person_nationalities.parquet"
WORK_SERIES_PQ: pathlib.Path = PARQUET_DIR / "work_series.parquet" # Placeholder
USER_INTERACTIONS_PQ: pathlib.Path = PARQUET_DIR / "user_interactions.parquet" # Placeholder

# --- Temporary Raw Parquet Filenames (Checkpoints) ---
PEOPLE_RAW_PQ: pathlib.Path = PARQUET_DIR / "people_raw_temp.parquet"
BOOKS_RAW_PQ: pathlib.Path = PARQUET_DIR / "books_raw_temp.parquet"
FILMS_RAW_PQ: pathlib.Path = PARQUET_DIR / "films_raw_temp.parquet"
COUNTRIES_RAW_PQ: pathlib.Path = PARQUET_DIR / "countries_raw_temp.parquet" # Example, maybe not needed if loaded directly
LANGUAGES_RAW_PQ: pathlib.Path = PARQUET_DIR / "languages_raw_temp.parquet" # Example

# === Column Definitions ===

# --- General Processing ---
DEFAULT_MULTI_VALUE_SEP: str = ";"
ID_START: int = 1 # Start IDs from 1

# --- People Columns ---
EXCEL_PEOPLE_HASH_ID: str = "Hash_ID"
EXCEL_PEOPLE_NAME: str = "Name"
EXCEL_PEOPLE_SURNAME: str = "Surname"
EXCEL_PEOPLE_REAL_NAME: str = "Real Name"
EXCEL_PEOPLE_TYPE: str = "Type"
EXCEL_PEOPLE_GENDER: str = "Gender"
EXCEL_PEOPLE_NATIONALITY: str = "Nationality" # Assumed to be in People sheet
EXCEL_PEOPLE_BIRTH_DAY: str = "Birth_Date_Day"
EXCEL_PEOPLE_BIRTH_MONTH: str = "Birth_Date_Month"
EXCEL_PEOPLE_BIRTH_YEAR: str = "Birth_Date_Year" # Non-Gregorian? Check usage.
EXCEL_PEOPLE_BIRTH_YEAR_GREG: str = "Birth_Date_Year_Gregorian" # Use this for parsing?
EXCEL_PEOPLE_BIRTH_RANGE: str = "Birth_Date_Year_IsRange"
EXCEL_PEOPLE_DEATH_DAY: str = "Death_Date_Day"
EXCEL_PEOPLE_DEATH_MONTH: str = "Death_Date_Month"
EXCEL_PEOPLE_DEATH_YEAR: str = "Death_Date_Year" # Non-Gregorian?
EXCEL_PEOPLE_DEATH_YEAR_GREG: str = "Death_Date_Year_Gregorian" # Use this?
EXCEL_PEOPLE_DEATH_RANGE: str = "Death_Date_Year_IsRange"

PEOPLE_EXCEL_COLS_NEEDED: List[str] = [
    # EXCEL_PEOPLE_HASH_ID, # Use index for now
    EXCEL_PEOPLE_NAME, EXCEL_PEOPLE_SURNAME,
    EXCEL_PEOPLE_REAL_NAME, EXCEL_PEOPLE_TYPE, EXCEL_PEOPLE_GENDER,
    EXCEL_PEOPLE_NATIONALITY, EXCEL_PEOPLE_BIRTH_DAY, EXCEL_PEOPLE_BIRTH_MONTH,
    EXCEL_PEOPLE_BIRTH_YEAR_GREG, EXCEL_PEOPLE_BIRTH_RANGE, EXCEL_PEOPLE_DEATH_DAY, # Assuming Gregorian Year
    EXCEL_PEOPLE_DEATH_MONTH, EXCEL_PEOPLE_DEATH_YEAR_GREG, EXCEL_PEOPLE_DEATH_RANGE
]
PEOPLE_RAW_SAVE_STR_COLS: Set[str] = {
    EXCEL_PEOPLE_BIRTH_YEAR,
    EXCEL_PEOPLE_DEATH_YEAR,
    EXCEL_PEOPLE_BIRTH_YEAR_GREG,
    EXCEL_PEOPLE_DEATH_YEAR_GREG,
    EXCEL_PEOPLE_BIRTH_DAY,
    EXCEL_PEOPLE_BIRTH_MONTH,
    EXCEL_PEOPLE_DEATH_DAY,
    EXCEL_PEOPLE_DEATH_MONTH,
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
PERSON_BIRTH_YEAR: str = "birth_year" # Primary parsed year
PERSON_BIRTH_DATE_ORIGINAL: str = "birth_date_original" # Raw string input
PERSON_BIRTH_DATE_QUALIFIER: str = "birth_date_qualifier" # circa, range, century
PERSON_DEATH_DATE: str = "death_date"
PERSON_DEATH_YEAR: str = "death_year"
PERSON_DEATH_DATE_ORIGINAL: str = "death_date_original"
PERSON_DEATH_DATE_QUALIFIER: str = "death_date_qualifier"

# Target 'person_nationalities' parquet/DB columns
NATIONALITY_PERSON_ID: str = "person_id"
NATIONALITY_COUNTRY_ID: str = "country_id"

# --- Books Columns ---
EXCEL_BOOKS_HASH_ID: str = "Hash_ID" # Maybe useful later for linking?
EXCEL_BOOKS_TITLE: str = "Title"
EXCEL_BOOKS_AUTHOR: str = "Author" # Multi-value ';'?
EXCEL_BOOKS_SERIES: str = "Series"
EXCEL_BOOKS_SERIES_NUMBER: str = "Series_Number"
EXCEL_BOOKS_PUBLISHED_DATE: str = "Published_Date" # Need parsing logic (year, maybe full date)
EXCEL_BOOKS_EDITION: str = "Edition" # Manifestation detail
EXCEL_BOOKS_PUBLISHER: str = "Publisher" # Manifestation detail
EXCEL_BOOKS_PUBLISHED_TITLE: str = "Published_Title" # Manifestation detail? Or subtitle?
EXCEL_BOOKS_PUBLISHED_LANGUAGE: str = "Published_Language" # Original or Edition language? Assume Original for Works for now.
EXCEL_BOOKS_PAGE_COUNT: str = "Page_Count" # Manifestation detail
EXCEL_BOOKS_DESCRIPTION: str = "Description_GenAI" # Map to works.description?
# User Interaction columns (Rating, Read, etc.) - map to user_interactions table later
# Identifier columns (Goodreads_URL, Hardcover_ID) - map to manifestations later

BOOKS_EXCEL_COLS_NEEDED: List[str] = [
    EXCEL_BOOKS_TITLE, EXCEL_BOOKS_AUTHOR, EXCEL_BOOKS_SERIES, EXCEL_BOOKS_SERIES_NUMBER,
    EXCEL_BOOKS_PUBLISHED_DATE, EXCEL_BOOKS_PUBLISHED_LANGUAGE, EXCEL_BOOKS_DESCRIPTION,
    # Add others if directly needed for Works table processing
]
BOOKS_RAW_SAVE_STR_COLS: Set[str] = {
    EXCEL_BOOKS_PUBLISHED_DATE, EXCEL_BOOKS_PAGE_COUNT, EXCEL_BOOKS_SERIES_NUMBER,
    EXCEL_BOOKS_AUTHOR, EXCEL_BOOKS_TITLE # Save ambiguous/multi-value as string
}

# --- Films Columns ---
EXCEL_FILMS_HASH_ID: str = "Hash_ID"
EXCEL_FILMS_TITLE: str = "Title"
EXCEL_FILMS_DIRECTOR: str = "Director" # Multi-value ';'?
EXCEL_FILMS_YEAR: str = "Year"
EXCEL_FILMS_COUNTRY: str = "Country" # Multi-value? Manifestation detail? Or work origin?

FILMS_EXCEL_COLS_NEEDED: List[str] = [
    EXCEL_FILMS_TITLE, EXCEL_FILMS_DIRECTOR, EXCEL_FILMS_YEAR, EXCEL_FILMS_COUNTRY
]
FILMS_RAW_SAVE_STR_COLS: Set[str] = {
    EXCEL_FILMS_YEAR, EXCEL_FILMS_DIRECTOR, EXCEL_FILMS_TITLE, EXCEL_FILMS_COUNTRY
}

# --- Countries Columns ---
# From Countries_Continents sheet
EXCEL_COUNTRY_NAME: str = "Country_Name"
EXCEL_COUNTRY_ALPHA2: str = "Two_Letter_Country_Code"
EXCEL_COUNTRY_ALPHA3: str = "Three_Letter_Country_Code"
EXCEL_COUNTRY_NUMBER: str = "Country_Number"
EXCEL_COUNTRY_CONTINENT_CODE: str = "Continent_Code"
EXCEL_COUNTRY_CONTINENT_NAME: str = "Continent_Name"

# Target 'countries' parquet/DB columns
COUNTRY_ID: str = "country_id"
COUNTRY_NAME: str = "name"
COUNTRY_ISO_ALPHA2: str = "iso_alpha2"
COUNTRY_ISO_ALPHA3: str = "iso_alpha3"
COUNTRY_NUMBER_COL: str = "country_number" # Renamed from 'number' to avoid SQL keyword conflict
COUNTRY_CONTINENT_CODE: str = "continent_code"
COUNTRY_CONTINENT_NAME: str = "continent_name"

# --- Languages Columns ---
EXCEL_LANG_HASH_ID: str = "Hash_ID" # Ignore?
EXCEL_LANG_NAME: str = "Language"
EXCEL_LANG_ISO1: str = "ISO_639-1"
EXCEL_LANG_ISO2: str = "ISO_639-2"
EXCEL_LANG_ISO3: str = "ISO_639-3"

# Target 'languages' parquet/DB columns
LANGUAGE_ID: str = "language_id"
LANGUAGE_NAME: str = "name"
LANGUAGE_ISO1: str = "iso_639_1"
LANGUAGE_ISO2: str = "iso_639_2"
LANGUAGE_ISO3: str = "iso_639_3"

# --- Work Types Columns ---
EXCEL_WORK_TYPE_NAME: str = "Name"
EXCEL_WORK_TYPE_DESC: str = "Description"

# Target 'work_types' parquet/DB columns
WORK_TYPE_ID: str = "work_type_id"
WORK_TYPE_NAME: str = "name"

# --- Contribution Types Columns ---
EXCEL_CONTRIB_TYPE_NAME: str = "Name"
EXCEL_CONTRIB_TYPE_DESC: str = "Description"

# Target 'contribution_types' parquet/DB columns
CONTRIB_TYPE_ID: str = "contribution_type_id"
CONTRIB_TYPE_NAME: str = "name"

# --- Works Columns (Target) ---
WORK_ID: str = "work_id"
WORK_WORK_TYPE_ID: str = "work_type_id"
WORK_PRIMARY_TITLE: str = "primary_title"
WORK_SUBTITLE: str = "subtitle" # Map from where? Maybe EXCEL_BOOKS_PUBLISHED_TITLE? TBD.
WORK_ORIG_LANG_ID: str = "original_language_id"
WORK_YEAR_START: str = "creation_year_start"
WORK_YEAR_END: str = "creation_year_end" # Handle ranges if needed
WORK_DESCRIPTION: str = "description"
# WORK_CREATED_AT: str = "created_at" # Handled by DB
# WORK_UPDATED_AT: str = "updated_at" # Handled by DB

# --- Work Contributors Columns (Target) ---
CONTRIB_WORK_ID: str = "work_id"
CONTRIB_PERSON_ID: str = "person_id"
CONTRIB_CONTRIB_TYPE_ID: str = "contribution_type_id"
CONTRIB_DETAILS: str = "contribution_details" # e.g. "uncredited" - TBD if needed

# Placeholder IDs/Names for common types (used until loaded from file)
# These should match the *exact* names in your Excel sheet for lookups
WORK_TYPE_BOOK_NAME: str = "Book"
WORK_TYPE_FILM_NAME: str = "Film"
CONTRIB_TYPE_AUTHOR_NAME: str = "Author"
CONTRIB_TYPE_DIRECTOR_NAME: str = "Director"
CONTRIB_TYPE_TRANSLATOR_NAME: str = "Translator" # Example