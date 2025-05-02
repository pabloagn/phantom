# phantom_canon/processing/books_processor.py
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

def _parse_creation_year(date_str: Optional[str]) -> Optional[int]:
    """Placeholder: Extracts year from various date formats."""
    if pd.isna(date_str) or date_str == "": return None
    try: return int(float(str(date_str).strip()))
    except ValueError:
        try:
            dt = pd.to_datetime(date_str, errors='coerce')
            if pd.notna(dt): return dt.year
        except Exception: pass
    log.debug(f"Could not parse year from date string: '{date_str}'")
    return None

def process_books(
    df_raw_books: pd.DataFrame,
    people_lookup: Dict[str, int], # Lowercased sort_name -> person_id
    people_display_lookup: Dict[str, int], # Lowercased display_name -> person_id
    lang_lookup: Dict[str, int],
    work_type_lookup: Dict[str, int],
    contrib_type_lookup: Dict[str, int],
    start_work_id: int
) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame], int]:
    """Transforms raw book data to 'works' and 'work_contributors'."""
    log.info(f"Processing {len(df_raw_books)} raw book entries...")
    df = df_raw_books.copy()
    works_records = []
    contributors_records = []
    current_work_id = start_work_id
    processed_count, contributors_added_count, match_attempts, match_success = 0, 0, 0, 0

    book_work_type_id = work_type_lookup.get(constants.WORK_TYPE_BOOK_NAME.lower())
    author_contrib_type_id = contrib_type_lookup.get(constants.CONTRIB_TYPE_AUTHOR_NAME.lower())

    if not book_work_type_id: log.error(f"Work Type ID '{constants.WORK_TYPE_BOOK_NAME}' not found."); return None, None, start_work_id
    if not author_contrib_type_id: log.error(f"Contrib Type ID '{constants.CONTRIB_TYPE_AUTHOR_NAME}' not found."); return None, None, start_work_id
    log.info(f"Using Book Work Type ID: {book_work_type_id}, Author Contrib Type ID: {author_contrib_type_id}")

    for index, row in df.iterrows():
        work_id = current_work_id
        title = row.get(constants.EXCEL_BOOKS_TITLE)
        if pd.isna(title) or str(title).strip() == "": log.warning(f"Skip book index {index}: missing title."); continue

        lang_name_raw = row.get(constants.EXCEL_BOOKS_PUBLISHED_LANGUAGE)
        lang_name_clean = _clean_name(lang_name_raw).lower() if pd.notna(lang_name_raw) else None
        orig_lang_id = lang_lookup.get(lang_name_clean) if lang_name_clean else None
        if lang_name_clean and not orig_lang_id: log.warning(f"WorkID {work_id} ('{str(title)[:50]}...'): Lang '{lang_name_raw}' not found.")

        creation_year = _parse_creation_year(row.get(constants.EXCEL_BOOKS_PUBLISHED_DATE))
        works_records.append({
            constants.WORK_ID: work_id, constants.WORK_WORK_TYPE_ID: book_work_type_id, constants.WORK_PRIMARY_TITLE: str(title).strip(),
            constants.WORK_SUBTITLE: None, constants.WORK_ORIG_LANG_ID: orig_lang_id, constants.WORK_YEAR_START: creation_year,
            constants.WORK_YEAR_END: None, constants.WORK_DESCRIPTION: row.get(constants.EXCEL_BOOKS_DESCRIPTION), })

        authors_str = row.get(constants.EXCEL_BOOKS_AUTHOR)
        if pd.notna(authors_str) and isinstance(authors_str, str) and authors_str.strip():
            authors = [a.strip() for a in authors_str.split(constants.DEFAULT_MULTI_VALUE_SEP) if a.strip()]
            for author_name_raw in authors:
                match_attempts += 1; person_id = None; lookup_method = "none"
                author_name_clean = _clean_name(author_name_raw)
                if not author_name_clean: continue

                primary_lookup_key = author_name_clean.lower()
                person_id = people_lookup.get(primary_lookup_key) # Try direct match with sort_name lookup first
                if person_id: lookup_method = "sort_name (direct)"
                else: # Fallback: try direct match with display_name lookup
                    person_id = people_display_lookup.get(primary_lookup_key)
                    if person_id: lookup_method = "display_name (direct)"

                if person_id:
                    contributors_records.append({ constants.CONTRIB_WORK_ID: work_id, constants.CONTRIB_PERSON_ID: person_id, constants.CONTRIB_CONTRIB_TYPE_ID: author_contrib_type_id, })
                    contributors_added_count += 1; match_success += 1
                    log.debug(f"WorkID {work_id}: Match '{author_name_raw}' -> P.{person_id} ({lookup_method} key='{primary_lookup_key}')")
                else:
                    log.warning(f"WorkID {work_id} ('{str(title)[:50]}...'): No match for Author '{author_name_raw}' (key='{primary_lookup_key}')")

        current_work_id += 1; processed_count += 1
        if processed_count % 500 == 0: log.info(f"Processed {processed_count}/{len(df)} book entries...")

    if not works_records: log.warning("No valid work records generated for books."); return None, None, start_work_id
    df_works_final = pd.DataFrame(works_records).astype({
        constants.WORK_ID: 'Int64', constants.WORK_WORK_TYPE_ID: 'Int64', constants.WORK_PRIMARY_TITLE: 'string', constants.WORK_SUBTITLE: 'string',
        constants.WORK_ORIG_LANG_ID: 'Int64', constants.WORK_YEAR_START: 'Int64', constants.WORK_YEAR_END: 'Int64', constants.WORK_DESCRIPTION: 'string', })
    df_contributors_final = pd.DataFrame(contributors_records)
    log.info(f"Finished books. Generated {len(df_works_final)} works. Matches: {match_success}/{match_attempts}. Links: {contributors_added_count}.")
    if match_attempts > 0 and match_success == 0: log.error("Author matching failed completely for books.")
    elif match_attempts > match_success: log.warning(f"Failed {match_attempts - match_success} author matches for books.")
    return df_works_final, df_contributors_final, current_work_id