import logging
import pandas as pd
import pathlib

# Assuming your constants are accessible (adjust if needed)
# If running this script directly, you might need to adjust sys.path or use relative imports carefully.
# For simplicity here, we assume constants.py can be found.
# A more robust way might involve making your phantom_canon package installable
# or adding the project root to PYTHONPATH.
try:
    from phantom_canon import constants, cli_display
except ImportError:
    # Simple fallback if running script directly from root and package isn't installed
    import sys
    # Add the project root to the path to find the phantom_canon package
    project_root = pathlib.Path(__file__).resolve().parent
    sys.path.insert(0, str(project_root))
    from phantom_canon import constants, cli_display

# Setup basic logging for the query script
logging.basicConfig(level="INFO", format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def query_books_by_author_lastname(target_lastname: str):
    """
    Queries the processed Parquet files to find books written by an author
    with the specified last name.

    Args:
        target_lastname: The last name of the author to search for (case-insensitive).
    """
    log.info(f"Starting query for books by author last name: '{target_lastname}'")

    required_files = {
        "people": constants.PEOPLE_PQ,
        "works": constants.WORKS_PQ,
        "contributors": constants.WORK_CONTRIBUTORS_PQ,
        "work_types": constants.WORK_TYPES_PQ,
        "contrib_types": constants.CONTRIBUTION_TYPES_PQ,
    }

    dfs = {}
    # --- 1. Load Required DataFrames ---
    log.info("Loading required Parquet files...")
    try:
        for name, path in required_files.items():
            if not path.exists():
                log.error(f"Required file not found: {path}. Aborting query.")
                return
            dfs[name] = pd.read_parquet(path)
            log.info(f"Loaded {name}.parquet ({len(dfs[name])} rows)")
    except Exception as e:
        log.error(f"Error loading Parquet files: {e}", exc_info=True)
        return

    df_people = dfs["people"]
    df_works = dfs["works"]
    df_contributors = dfs["contributors"]
    df_work_types = dfs["work_types"]
    df_contrib_types = dfs["contrib_types"]

    # --- 2. Find the Target Person ID(s) ---
    log.info(f"Finding person IDs for last name '{target_lastname}'...")
    target_lastname_lower = target_lastname.lower()
    target_people = df_people[
        df_people[constants.PERSON_LAST_NAME].str.lower() == target_lastname_lower
    ]

    if target_people.empty:
        log.warning(f"No person found with last name '{target_lastname}'.")
        print(f"\nNo person found with last name '{target_lastname}'.")
        return

    target_person_ids = target_people[constants.PERSON_ID].tolist()
    log.info(f"Found {len(target_person_ids)} person ID(s): {target_person_ids}")
    print(f"\nFound people matching '{target_lastname}':")
    print(target_people[[constants.PERSON_ID, constants.PERSON_DISPLAY_NAME]].to_string(index=False))


    # --- 3. Find the Contribution Type ID for 'Author' ---
    log.info("Finding contribution type ID for 'Author'...")
    author_contrib_name_lower = constants.CONTRIB_TYPE_AUTHOR_NAME.lower()
    author_type = df_contrib_types[
        df_contrib_types[constants.CONTRIB_TYPE_NAME].str.lower() == author_contrib_name_lower
    ]

    if author_type.empty:
        log.error(f"Contribution type '{constants.CONTRIB_TYPE_AUTHOR_NAME}' not found in contribution_types.parquet. Aborting.")
        return

    author_type_id = author_type[constants.CONTRIB_TYPE_ID].iloc[0]
    log.info(f"Found 'Author' contribution type ID: {author_type_id}")

    # --- 4. Find the Work Type ID for 'Book' ---
    log.info("Finding work type ID for 'Book'...")
    book_work_type_lower = constants.WORK_TYPE_BOOK_NAME.lower()
    book_type = df_work_types[
        df_work_types[constants.WORK_TYPE_NAME].str.lower() == book_work_type_lower
    ]

    if book_type.empty:
        log.error(f"Work type '{constants.WORK_TYPE_BOOK_NAME}' not found in work_types.parquet. Aborting.")
        return

    book_type_id = book_type[constants.WORK_TYPE_ID].iloc[0]
    log.info(f"Found 'Book' work type ID: {book_type_id}")


    # --- 5. Filter Contributions ---
    # Find contributions made by the target person(s) AS an Author
    log.info("Filtering contributions...")
    target_contributions = df_contributors[
        (df_contributors[constants.CONTRIB_PERSON_ID].isin(target_person_ids)) &
        (df_contributors[constants.CONTRIB_CONTRIB_TYPE_ID] == author_type_id)
    ]

    if target_contributions.empty:
        log.warning(f"No contributions found for person ID(s) {target_person_ids} with contribution type 'Author' ({author_type_id}).")
        print(f"\nNo works found where '{target_lastname}' contributed as an Author.")
        return

    target_work_ids = target_contributions[constants.CONTRIB_WORK_ID].unique().tolist()
    log.info(f"Found {len(target_work_ids)} potential work ID(s) contributed to by the target author(s).")


    # --- 6. Filter Works ---
    # Find works that match the target work IDs AND are of type 'Book'
    log.info("Filtering works...")
    target_works = df_works[
        (df_works[constants.WORK_ID].isin(target_work_ids)) &
        (df_works[constants.WORK_WORK_TYPE_ID] == book_type_id)
    ]

    if target_works.empty:
        log.warning(f"Found contributions by '{target_lastname}' but none were associated with works of type 'Book' ({book_type_id}).")
        print(f"\nNo Books found where '{target_lastname}' contributed as an Author.")
        return

    log.info(f"Found {len(target_works)} Book(s) matching the criteria.")

    # --- 7. Combine and Display Results ---
    # Merge works with the people info for better display (optional but helpful)
    # We only need the specific contributions by our target author for context
    final_results = pd.merge(
        target_works[[constants.WORK_ID, constants.WORK_PRIMARY_TITLE, constants.WORK_YEAR_START]],
        target_contributions[[constants.CONTRIB_WORK_ID, constants.CONTRIB_PERSON_ID]],
        on=constants.CONTRIB_WORK_ID
    )
    # Add the display name back
    final_results = pd.merge(
        final_results,
        target_people[[constants.PERSON_ID, constants.PERSON_DISPLAY_NAME]],
        on=constants.PERSON_ID
    )

    # Select and order columns for display
    display_cols = [
        constants.WORK_ID,
        constants.WORK_PRIMARY_TITLE,
        constants.PERSON_DISPLAY_NAME,
        constants.WORK_YEAR_START
    ]
    final_results = final_results[display_cols].drop_duplicates().sort_values(by=constants.WORK_PRIMARY_TITLE)


    print(f"\n--- Books written by authors with last name '{target_lastname}' ---")
    if not final_results.empty:
        print(final_results.to_string(index=False))
    else:
        # This case should ideally be caught earlier, but as a fallback:
        print("No matching books found after final filtering.")
    print(f"-----------------------------------------------------------------")


# --- Example Usage ---
if __name__ == "__main__":
    # Specify the last name you want to search for
    author_lastname_to_find = "Sebald"
    query_books_by_author_lastname(author_lastname_to_find)

    author_lastname_to_find = "Deleuze"
    query_books_by_author_lastname(author_lastname_to_find)