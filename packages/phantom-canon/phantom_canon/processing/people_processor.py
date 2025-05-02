# phantom_canon/processing/people_processor.py
import logging
import re
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from phantom_canon import constants

log = logging.getLogger(__name__)

# --- Helper Functions (_parse_year, _parse_full_date) ---
def _parse_year(year_str: Optional[str]) -> Tuple[Optional[int], Optional[str]]:
    """Parses a year string, handling integers, 'circa', ranges, centuries."""
    if pd.isna(year_str) or not isinstance(year_str, str) or year_str.strip() == "":
        return None, None
    year_str = year_str.strip()
    qualifier = None
    year_int = None

    # Handle BCE/BC explicitly first if present, treat as negative years
    is_bce = False
    if "bce" in year_str.lower() or "bc" in year_str.lower():
        is_bce = True
        year_str = re.sub(r"\s*(bce|bc)\s*", "", year_str, flags=re.IGNORECASE).strip()

    if year_str.lower().startswith("c.") or year_str.lower().startswith("circa"):
        qualifier = "circa"
        year_str = re.sub(r"^[Cc](irca|\.)\s*", "", year_str).strip()

    range_match = re.match(r"^(\d{1,4})\s*[-–—]\s*(\d{1,4})$", year_str) # Handle different dashes
    if range_match:
        qualifier = qualifier or "range"
        try: year_int = int(range_match.group(1)) # Use start year of range
        except ValueError: pass

    century_match = re.match(r"^(?:(\d{1,2})(?:st|nd|rd|th))?\s*[Cc]entury$", year_str, re.IGNORECASE)
    if century_match:
        qualifier = qualifier or "century"
        try:
             century_num = int(century_match.group(1))
             # Estimate: start year of the century for consistency
             # year_int = (century_num * 100) - 99 # Start of century
             year_int = (century_num - 1) * 100 + 1 # Start year (e.g., 5th century -> 401)

        except (ValueError, TypeError): pass

    # Catch simple year numbers if not caught by other patterns
    if year_int is None:
        simple_year_match = re.match(r"^(\d{1,4})$", year_str)
        if simple_year_match:
            try: year_int = int(simple_year_match.group(1))
            except (ValueError, TypeError): pass

    # Fallback attempt for any remaining digits after cleaning
    if year_int is None:
         cleaned_year_str = re.sub(r"[^\d]", "", year_str) # Remove non-digits
         if cleaned_year_str:
              try: year_int = int(cleaned_year_str)
              except (ValueError, TypeError): log.debug(f"Could not parse year '{year_str}' to int after cleaning.")

    # Apply BCE sign
    if year_int is not None and is_bce:
        year_int = -year_int

    # Range check
    if year_int is not None and (year_int < -5000 or year_int > 2100): # Adjusted range slightly
        log.debug(f"Parsed year {year_int} from '{year_str}' out of reasonable range.")
        year_int = None

    return year_int, qualifier

def _parse_full_date(d: Optional[str], m: Optional[str], y: Optional[str]) -> Tuple[Optional[pd.Timestamp], Optional[int], Optional[str], Optional[str]]:
    """Attempts to parse day, month, year into a Timestamp and extracts year/qualifier."""
    original_parts = [str(p) for p in [d, m, y] if pd.notna(p) and str(p).strip() != ""]
    original_str = " / ".join(original_parts) if original_parts else None

    # Use the specific Gregorian year column if available for parsing, otherwise fall back
    year_to_parse = y # Assume the primary year column contains parseable info
    # If you have a separate _GREG column and want to prioritize it:
    # year_to_parse = y_greg if pd.notna(y_greg) else y # Example

    year_int, qualifier = _parse_year(str(year_to_parse) if pd.notna(year_to_parse) else None)

    timestamp = pd.NaT
    if pd.notna(d) and pd.notna(m) and year_int is not None and year_int > 0: # Parsing full date for BCE is tricky
         try:
             # Ensure d/m are clean integers
             clean_d = int(float(d))
             clean_m = int(float(m))
             date_str = f"{int(year_int)}-{clean_m:02d}-{clean_d:02d}"
             timestamp = pd.to_datetime(date_str, errors='coerce')
             # Add qualifier back if parsing succeeded but original year had one
             if pd.notna(timestamp) and qualifier:
                  log.debug(f"Full date parsed for {date_str}, but original year had qualifier '{qualifier}'. Retaining qualifier.")
             else:
                  qualifier = None # If we have a full date, qualifier usually becomes redundant

         except (ValueError, TypeError):
             timestamp = pd.NaT
             # If full date parse fails, stick with year_int and original qualifier
             log.debug(f"Could not parse full date: d='{d}', m='{m}', y='{y}' (parsed year_int={year_int})")


    # If no full date, create approximate timestamp from year (Jan 1st) for sorting purposes
    if pd.isna(timestamp) and year_int is not None:
         try:
             # Handle BCE year approximation - use end of year? (e.g., -428 -> -428-12-31)
             # For simplicity, pandas might handle negative years in to_datetime directly if format is right
             # Let's try YYYY-01-01 format. pandas < 2.0 might struggle with BCE.
              timestamp = pd.to_datetime(f"{year_int}-01-01", errors='coerce')
         except ValueError:
             timestamp = pd.NaT

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

    log.info(f"Processing {len(df_raw)} raw people entries...")
    df = df_raw.copy()

    # Ensure source columns exist, fill with NA if not
    required_raw_cols = [
        constants.EXCEL_PEOPLE_NAME, constants.EXCEL_PEOPLE_SURNAME,
        constants.EXCEL_PEOPLE_REAL_NAME, constants.EXCEL_PEOPLE_GENDER,
        constants.EXCEL_PEOPLE_NATIONALITY, constants.EXCEL_PEOPLE_BIRTH_DAY,
        constants.EXCEL_PEOPLE_BIRTH_MONTH, constants.EXCEL_PEOPLE_BIRTH_YEAR_GREG, # Prioritize Gregorian if available
        constants.EXCEL_PEOPLE_DEATH_DAY, constants.EXCEL_PEOPLE_DEATH_MONTH,
        constants.EXCEL_PEOPLE_DEATH_YEAR_GREG, # Prioritize Gregorian if available
    ]
    for col in required_raw_cols:
        if col not in df.columns:
            log.warning(f"Expected raw column '{col}' not found. Filling with NA.")
            df[col] = pd.NA

    # 1. Generate Unique Person ID
    df = df.reset_index().rename(columns={"index": constants.PERSON_ID})
    df[constants.PERSON_ID] = df[constants.PERSON_ID] + constants.ID_START
    df[constants.PERSON_ID] = df[constants.PERSON_ID].astype('Int64')

    # 2. Parse Names
    df[constants.PERSON_FIRST_NAME] = df[constants.EXCEL_PEOPLE_NAME].fillna('').astype(str).str.strip()
    df[constants.PERSON_LAST_NAME] = df[constants.EXCEL_PEOPLE_SURNAME].fillna('').astype(str).str.strip()
    # Use NA instead of empty string for potentially missing names
    df[constants.PERSON_FIRST_NAME] = df[constants.PERSON_FIRST_NAME].replace('', pd.NA).astype("string")
    df[constants.PERSON_LAST_NAME] = df[constants.PERSON_LAST_NAME].replace('', pd.NA).astype("string")
    df[constants.PERSON_BIRTH_NAME] = df[constants.EXCEL_PEOPLE_REAL_NAME].fillna('').astype(str).str.strip()
    df[constants.PERSON_BIRTH_NAME] = df[constants.PERSON_BIRTH_NAME].replace('', pd.NA).astype("string")

    # Create Display Name and Sort Name
    def create_display_name(row):
        first = row[constants.PERSON_FIRST_NAME]
        last = row[constants.PERSON_LAST_NAME]
        if pd.notna(first) and pd.notna(last): return f"{first} {last}"
        if pd.notna(first): return first
        if pd.notna(last): return last
        return pd.NA # Or maybe "Unknown Person"?

    def create_sort_name(row):
        first = row[constants.PERSON_FIRST_NAME]
        last = row[constants.PERSON_LAST_NAME]
        if pd.notna(last) and pd.notna(first): return f"{last}, {first}"
        if pd.notna(last): return last # Sort by last name if first is missing
        if pd.notna(first): return first # Sort by first name if last is missing
        return pd.NA

    df[constants.PERSON_DISPLAY_NAME] = df.apply(create_display_name, axis=1).astype("string")
    df[constants.PERSON_SORT_NAME] = df.apply(create_sort_name, axis=1).astype("string")

    # Ensure display/sort names are not NA if possible (critical for lookups)
    df[constants.PERSON_DISPLAY_NAME] = df[constants.PERSON_DISPLAY_NAME].fillna(f"Person_{df[constants.PERSON_ID]}").astype("string")
    df[constants.PERSON_SORT_NAME] = df[constants.PERSON_SORT_NAME].fillna(df[constants.PERSON_DISPLAY_NAME]).astype("string")

    # 3. Parse Dates
    # Decide which year column to use (Gregorian preferred if exists)
    birth_year_col = constants.EXCEL_PEOPLE_BIRTH_YEAR_GREG if constants.EXCEL_PEOPLE_BIRTH_YEAR_GREG in df.columns else constants.EXCEL_PEOPLE_BIRTH_YEAR
    death_year_col = constants.EXCEL_PEOPLE_DEATH_YEAR_GREG if constants.EXCEL_PEOPLE_DEATH_YEAR_GREG in df.columns else constants.EXCEL_PEOPLE_DEATH_YEAR

    birth_info = df.apply(lambda r: _parse_full_date(
        r.get(constants.EXCEL_PEOPLE_BIRTH_DAY),
        r.get(constants.EXCEL_PEOPLE_BIRTH_MONTH),
        r.get(birth_year_col)), # Use determined year column
        axis=1, result_type='expand')
    df[[constants.PERSON_BIRTH_DATE, constants.PERSON_BIRTH_YEAR, constants.PERSON_BIRTH_DATE_ORIGINAL, constants.PERSON_BIRTH_DATE_QUALIFIER]] = birth_info

    death_info = df.apply(lambda r: _parse_full_date(
        r.get(constants.EXCEL_PEOPLE_DEATH_DAY),
        r.get(constants.EXCEL_PEOPLE_DEATH_MONTH),
        r.get(death_year_col)), # Use determined year column
        axis=1, result_type='expand')
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
    df[constants.PERSON_GENDER] = df[constants.PERSON_GENDER].replace('', 'Unknown').astype("string") # Use category later?

    # 5. Process Nationalities (Junction Table)
    nationalities_records = []
    country_lookup = {}
    # Corrected check: Use the *final* column name (constants.COUNTRY_NAME)
    if df_countries is not None and constants.COUNTRY_NAME in df_countries.columns and constants.COUNTRY_ID in df_countries.columns:
        # Build lookup cache: lowercase final name -> ID
        country_lookup = df_countries.set_index(df_countries[constants.COUNTRY_NAME].str.lower().str.strip())[constants.COUNTRY_ID].to_dict()
        log.info(f"Created country lookup with {len(country_lookup)} entries.")
    else:
        log.warning("Cannot create country lookup map. Required columns ('name', 'country_id') not found in the provided countries DataFrame.")
        if df_countries is not None:
             log.warning(f"Available columns in df_countries: {df_countries.columns.tolist()}")
        else:
             log.warning("df_countries DataFrame itself is None.")


    if country_lookup and constants.EXCEL_PEOPLE_NATIONALITY in df.columns: # Only proceed if lookup exists AND column exists
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
                        log.warning(f"Could not map nationality '{nat_name_lower}' to a country ID for person_id {person_id}.")
    elif not country_lookup:
         log.warning("Skipping nationality processing because country lookup is empty.")
    else: # country_lookup exists but column doesn't
         log.warning(f"Skipping nationality processing because column '{constants.EXCEL_PEOPLE_NATIONALITY}' not found in raw people data.")

    df_person_nationalities = pd.DataFrame(nationalities_records).drop_duplicates()
    if not df_person_nationalities.empty:
        df_person_nationalities = df_person_nationalities.astype({
            constants.NATIONALITY_PERSON_ID: 'Int64',
            constants.NATIONALITY_COUNTRY_ID: 'Int64'
        })
        log.info(f"Created {len(df_person_nationalities)} person-nationality links.")
    else:
         log.info("Created 0 person-nationality links.")


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
            log.warning(f"Target column '{col}' was not generated during processing. Adding as NA.")
            df[col] = pd.NA # Or appropriate default

    df_people_final = df[final_people_cols].copy() # Use copy to avoid SettingWithCopyWarning
    log.info(f"Final people DataFrame created with {len(df_people_final)} rows and columns: {df_people_final.columns.tolist()}")

    # Final type check/conversion just before returning
    df_people_final = df_people_final.astype({
         constants.PERSON_ID: 'Int64',
         constants.PERSON_FIRST_NAME: 'string',
         constants.PERSON_LAST_NAME: 'string',
         constants.PERSON_SORT_NAME: 'string',
         constants.PERSON_DISPLAY_NAME: 'string',
         constants.PERSON_BIRTH_NAME: 'string',
         constants.PERSON_GENDER: 'string',
         constants.PERSON_BIRTH_DATE: 'datetime64[ns]',
         constants.PERSON_BIRTH_YEAR: 'Int64',
         constants.PERSON_BIRTH_DATE_ORIGINAL: 'string',
         constants.PERSON_BIRTH_DATE_QUALIFIER: 'string',
         constants.PERSON_DEATH_DATE: 'datetime64[ns]',
         constants.PERSON_DEATH_YEAR: 'Int64',
         constants.PERSON_DEATH_DATE_ORIGINAL: 'string',
         constants.PERSON_DEATH_DATE_QUALIFIER: 'string'
    })


    return df_people_final, df_person_nationalities