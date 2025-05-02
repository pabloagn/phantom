# phantom_canon/processing/films_processor.py
      
import logging
import re
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from phantom_canon import constants, cli_display

log = logging.getLogger(__name__)

def _clean_name(name: Optional[str]) -> Optional[str]:
    """Basic name cleaning."""
    if pd.isna(name) or not isinstance(name, str): return None
    cleaned_name = ' '.join(name.split())
    return cleaned_name.strip()

def _parse_creation_year(year_val: Optional[str]) -> Optional[int]:
    """Placeholder: Extracts year."""
    if pd.isna(year_val) or year_val == "": return None
    try: return int(float(str(year_val).strip()))
    except ValueError: log.debug(f"Could not parse film year: '{year_val}'"); return None

def process_films(
    df_raw_films: pd.DataFrame,
    people_lookup: Dict[str, int],
    people_display_lookup: Dict[str, int],
    lang_lookup: Dict[str, int],
    work_type_lookup: Dict[str, int],
    contrib_type_lookup: Dict[str, int],
    start_work_id: int
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], int]:
    """Transforms raw film data to 'works' and 'work_contributors'."""
    log.info(f"Processing {len(df_raw_films)} raw film entries...")
    df = df_raw_films.copy()
    works_records = []
    contributors_records = []
    current_work_id = start_work_id
    processed_count, contributors_added_count, match_attempts, match_success = 0, 0, 0, 0

    film_work_type_id = work_type_lookup.get(constants.WORK_TYPE_FILM_NAME.lower())
    director_contrib_type_id = contrib_type_lookup.get(constants.CONTRIB_TYPE_DIRECTOR_NAME.lower())

    if not film_work_type_id: log.error(f"Work Type ID '{constants.WORK_TYPE_FILM_NAME}' not found."); return None, None, start_work_id
    if not director_contrib_type_id: log.error(f"Contrib Type ID '{constants.CONTRIB_TYPE_DIRECTOR_NAME}' not found."); return None, None, start_work_id
    log.info(f"Using Film Work Type ID: {film_work_type_id}, Director Contrib Type ID: {director_contrib_type_id}")

    for index, row in df.iterrows():
        work_id = current_work_id
        title = row.get(constants.EXCEL_FILMS_TITLE)
        if pd.isna(title) or str(title).strip() == "": log.warning(f"Skip film index {index}: missing title."); continue

        orig_lang_id = None # Assuming no language info for films yet
        creation_year = _parse_creation_year(row.get(constants.EXCEL_FILMS_YEAR))
        works_records.append({
            constants.WORK_ID: work_id, constants.WORK_WORK_TYPE_ID: film_work_type_id, constants.WORK_PRIMARY_TITLE: str(title).strip(),
            constants.WORK_SUBTITLE: None, constants.WORK_ORIG_LANG_ID: orig_lang_id, constants.WORK_YEAR_START: creation_year,
            constants.WORK_YEAR_END: None, constants.WORK_DESCRIPTION: None, })

        directors_str = row.get(constants.EXCEL_FILMS_DIRECTOR)
        if pd.notna(directors_str) and isinstance(directors_str, str) and directors_str.strip():
            directors = [d.strip() for d in directors_str.split(constants.DEFAULT_MULTI_VALUE_SEP) if d.strip()]
            for director_name_raw in directors:
                match_attempts += 1; person_id = None; lookup_method = "none"
                director_name_clean = _clean_name(director_name_raw)
                if not director_name_clean: continue

                primary_lookup_key = director_name_clean.lower()
                person_id = people_lookup.get(primary_lookup_key)
                if person_id: lookup_method = "sort_name (direct)"
                else:
                    person_id = people_display_lookup.get(primary_lookup_key)
                    if person_id: lookup_method = "display_name (direct)"

                if person_id:
                    contributors_records.append({ constants.CONTRIB_WORK_ID: work_id, constants.CONTRIB_PERSON_ID: person_id, constants.CONTRIB_CONTRIB_TYPE_ID: director_contrib_type_id, })
                    contributors_added_count += 1; match_success += 1
                    log.debug(f"WorkID {work_id}: Match '{director_name_raw}' -> P.{person_id} ({lookup_method} key='{primary_lookup_key}')")
                else:
                    log.warning(f"WorkID {work_id} ('{str(title)[:50]}...'): No match for Director '{director_name_raw}' (key='{primary_lookup_key}')")

        current_work_id += 1; processed_count += 1
        if processed_count % 100 == 0: log.info(f"Processed {processed_count}/{len(df)} film entries...")

    if not works_records: log.warning("No valid work records generated for films."); return None, None, start_work_id
    df_works_final = pd.DataFrame(works_records).astype({
        constants.WORK_ID: 'Int64', constants.WORK_WORK_TYPE_ID: 'Int64', constants.WORK_PRIMARY_TITLE: 'string', constants.WORK_SUBTITLE: 'string',
        constants.WORK_ORIG_LANG_ID: 'Int64', constants.WORK_YEAR_START: 'Int64', constants.WORK_YEAR_END: 'Int64', constants.WORK_DESCRIPTION: 'string', })
    df_contributors_final = pd.DataFrame(contributors_records)
    log.info(f"Finished films. Generated {len(df_works_final)} works. Matches: {match_success}/{match_attempts}. Links: {contributors_added_count}.")
    if match_attempts > 0 and match_success == 0: log.error("Director matching failed completely for films.")
    elif match_attempts > match_success: log.warning(f"Failed {match_attempts - match_success} director matches for films.")
    return df_works_final, df_contributors_final, current_work_id