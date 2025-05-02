# phantom_enrichment/core/orchestrator.py

import time
import json
import pandas as pd
from typing import Dict, Any, List, Optional
from loguru import logger
from rapidfuzz import fuzz, process
import importlib # Used to dynamically get scorer function

# Project specific imports
from phantom_enrichment.config.settings import Settings
from phantom_enrichment.enrichment.providers.isbndb_client import IsbnDbClient
from phantom_enrichment.utils.helpers import normalize_string, generate_book_id
from phantom_enrichment.utils.exceptions import EnrichmentError, ProviderApiError, ConfigurationError

class Orchestrator:
    """
    Coordinates the media enrichment process.

    Reads input data, interacts with configured API providers via clients,
    applies matching logic, extracts relevant fields based on configuration,
    and returns the enriched data.
    """

    def __init__(self, settings: Settings, api_fields_config: Dict[str, Any]):
        """
        Initializes the Orchestrator.

        Args:
            settings: The application settings object.
            api_fields_config: The loaded configuration mapping output fields
                               to provider-specific fields.
        """
        self.settings = settings
        self.api_fields_config = api_fields_config
        self.clients = self._initialize_clients()

        # Validate fuzzy scorer name from settings
        self.fuzzy_scorer_func = self._get_fuzzy_scorer(settings.fuzzy_scorer)

        logger.info("Orchestrator initialized.")

    def _initialize_clients(self) -> Dict[str, Any]:
        """Initializes API client instances based on settings."""
        clients = {}
        # --- Initialize ISBNDB Client ---
        try:
            isbndb_client = IsbnDbClient(
                api_key=self.settings.isbndb_api_key.get_secret_value(),
                base_url=str(self.settings.isbndb_base_url)
                # Pass rate_limit_delay explicitly if needed, otherwise uses client default
            )
            clients["isbndb"] = isbndb_client
            logger.info("ISBNDB client successfully initialized in Orchestrator.")
        except ConfigurationError as e:
            logger.error(f"Failed to initialize ISBNDB client: {e}")
            # Decide if this is critical - maybe allow running without some clients?
            # For now, let's assume ISBNDB is needed if requested.
        except Exception as e:
            logger.exception("Unexpected error initializing ISBNDB client.")

        # --- Initialize other clients here (e.g., Hardcover) ---
        # try:
        #     hardcover_client = HardcoverClient(...)
        #     clients["hardcover"] = hardcover_client
        # except ConfigurationError as e:
        #     logger.error(f"Failed to initialize Hardcover client: {e}")

        return clients

    def _get_fuzzy_scorer(self, scorer_name: str) -> callable:
        """Gets the specified fuzzy matching function from rapidfuzz."""
        try:
            # Attempt to get the function from rapidfuzz.fuzz module
            scorer_func = getattr(fuzz, scorer_name)
            if not callable(scorer_func):
                raise AttributeError # Not a function
            logger.info(f"Using fuzzy scorer: rapidfuzz.fuzz.{scorer_name}")
            return scorer_func
        except AttributeError:
            default_scorer = 'token_sort_ratio'
            logger.warning(
                f"Invalid fuzzy scorer '{scorer_name}' specified in settings. "
                f"Falling back to default: '{default_scorer}'."
            )
            return getattr(fuzz, default_scorer) # Fallback to a reliable default
        except Exception as e:
             default_scorer = 'token_sort_ratio'
             logger.exception(f"Unexpected error getting fuzzy scorer '{scorer_name}'. Falling back to default: '{default_scorer}'. Error: {e}")
             return getattr(fuzz, default_scorer)


    def enrich_books(
        self,
        input_df: pd.DataFrame,
        providers: List[str] = ["isbndb"]
    ) -> Optional[pd.DataFrame]:
        """
        Enriches book data from the input DataFrame using specified providers.

        Args:
            input_df: DataFrame containing book data with columns 'Title' and 'Author'.
            providers: A list of provider names (e.g., ["isbndb"]) to use for enrichment.

        Returns:
            A DataFrame containing the enriched edition data for matched books,
            or None if no enrichment could be performed.
        """
        if input_df.empty:
            logger.warning("Input DataFrame is empty. No enrichment to perform.")
            return None
        if not all(col in input_df.columns for col in ['Title', 'Author']):
            logger.error("Input DataFrame must contain 'Title' and 'Author' columns.")
            raise ValueError("Input DataFrame missing required columns: 'Title', 'Author'")

        all_enriched_data = []
        valid_providers = [p for p in providers if p in self.clients]

        if not valid_providers:
            logger.error(f"No valid or initialized clients found for requested providers: {providers}. Cannot enrich.")
            return None

        logger.info(f"Starting book enrichment using providers: {valid_providers}")

        for provider in valid_providers:
            logger.info(f"--- Processing with provider: {provider} ---")
            if provider == "isbndb":
                try:
                    provider_results = self._enrich_with_isbndb(input_df)
                    if provider_results is not None and not provider_results.empty:
                        all_enriched_data.append(provider_results)
                    else:
                        logger.warning(f"Provider '{provider}' yielded no enriched data.")
                except Exception as e:
                    logger.exception(f"Error during enrichment with provider '{provider}'. Skipping this provider.")
            # Add elif blocks for other providers (e.g., hardcover)
            # elif provider == "hardcover":
            #     provider_results = self._enrich_with_hardcover(input_df)
            #     ...
            else:
                logger.warning(f"Enrichment logic for provider '{provider}' is not implemented.")

        if not all_enriched_data:
            logger.warning("Enrichment process completed, but no data was collected from any provider.")
            return None

        # Combine results from different providers if necessary (simple concat for now)
        # More sophisticated merging might be needed later if multiple providers return data for the same edition
        final_df = pd.concat(all_enriched_data, ignore_index=True)
        logger.success(f"Enrichment process completed. Collected {len(final_df)} edition records.")
        return final_df


    def _enrich_with_isbndb(self, input_df: pd.DataFrame) -> Optional[pd.DataFrame]:
        """Handles the enrichment process specifically for the ISBNDB provider."""
        isbndb_client: IsbnDbClient = self.clients.get("isbndb")
        if not isbndb_client:
            logger.error("ISBNDB client not available in Orchestrator.")
            return None # Cannot proceed without the client

        # Get ISBNDB specific field config
        try:
             # Navigate the config structure safely
            provider_config = self.api_fields_config.get("books", {}).get("isbndb", {})
            if not provider_config or "fields_to_extract" not in provider_config:
                 raise KeyError("ISBNDB field configuration missing or incomplete.")
            isbndb_field_map = provider_config["fields_to_extract"]
            list_fields = provider_config.get("list_fields", [])
            object_fields = provider_config.get("object_fields", [])
        except KeyError as e:
            logger.error(f"Missing configuration for ISBNDB: {e}")
            raise ConfigurationError(f"ISBNDB configuration error: {e}")

        all_matched_editions = []
        total_rows = len(input_df)

        for index, row in input_df.iterrows():
            input_title = row.get('Title')
            input_author = row.get('Author')
            book_id = generate_book_id(input_title, input_author) # Use helper

            logger.info(f"Processing row {index + 1}/{total_rows}: Book ID '{book_id}' (Title: '{input_title}', Author: '{input_author}')")

            if not input_title or not input_author:
                logger.warning(f"Skipping row {index + 1} due to missing Title or Author. Book ID: '{book_id}'")
                continue

            try:
                # Pass relevant configs to the row processing method
                matched_editions_for_row = self._process_book_row_isbndb(
                    input_title=input_title,
                    input_author=input_author,
                    book_id=book_id,
                    isbndb_client=isbndb_client,
                    isbndb_field_map=isbndb_field_map,
                    list_fields=list_fields,
                    object_fields=object_fields
                )
                if matched_editions_for_row:
                    all_matched_editions.extend(matched_editions_for_row)
                    logger.info(f"Found {len(matched_editions_for_row)} matching edition(s) for Book ID '{book_id}'.")
                else:
                     logger.warning(f"No matching editions found for Book ID '{book_id}' based on criteria.")

            except Exception as e:
                # Catch unexpected errors during row processing, log, and continue
                logger.exception(f"Unexpected error processing Book ID '{book_id}'. Skipping row.")
                # Optionally add this error to a separate error log/report

        if not all_matched_editions:
            return None

        return pd.DataFrame(all_matched_editions)


    def _process_book_row_isbndb(
        self,
        input_title: str,
        input_author: str,
        book_id: str,
        isbndb_client: IsbnDbClient,
        isbndb_field_map: Dict[str, str],
        list_fields: List[str],
        object_fields: List[str]
    ) -> List[Dict[str, Any]]:
        """Searches ISBNDB for a single book, filters candidates, and extracts data."""
        search_query = f"{input_title} {input_author}"
        matched_editions = []
        fetch_timestamp = pd.Timestamp.utcnow() # Use UTC timestamp

        try:
            logger.debug(f"Book ID '{book_id}': Searching ISBNDB with query '{search_query}', page size {self.settings.initial_search_page_size}")
            search_results = isbndb_client.search_books(
                query=search_query,
                page=1,
                page_size=self.settings.initial_search_page_size
            )
        except ProviderApiError as e:
            logger.error(f"Book ID '{book_id}': API error during ISBNDB search: {e}")
            return [] # Return empty list on API failure for this book
        except ValueError as e:
             logger.error(f"Book ID '{book_id}': Invalid parameters for ISBNDB search: {e}")
             return []

        candidate_books = search_results.get("books", [])
        total_candidates = search_results.get("total", len(candidate_books))
        logger.debug(f"Book ID '{book_id}': Received {len(candidate_books)} candidates (Total reported: {total_candidates}). Filtering based on matching type '{self.settings.matching_type}'.")

        if not candidate_books:
            return [] # No candidates found

        # Normalize input once for efficiency
        norm_input_title = normalize_string(input_title)
        norm_input_author = normalize_string(input_author)
        # Handle "Surname, Name" in input author for matching
        if ',' in norm_input_author:
             norm_input_author = norm_input_author.split(',')[0].strip()


        for candidate in candidate_books:
            candidate_title = candidate.get("title")
            candidate_authors_list = candidate.get("authors", []) # Expecting a list

            # --- Perform Matching ---
            is_match, details = self._check_match(
                norm_input_title=norm_input_title,
                norm_input_author=norm_input_author,
                candidate_title=candidate_title,
                candidate_authors_list=candidate_authors_list
            )

            candidate_isbn13 = candidate.get("isbn13", "N/A")
            logger.trace(f"Book ID '{book_id}', Candidate ISBN '{candidate_isbn13}': Title='{candidate_title}', Authors={candidate_authors_list}. Match Result: {is_match}. Details: {details}")

            if is_match:
                # --- Extract Data for Matched Edition ---
                try:
                    extracted_data = self._extract_edition_data(
                        candidate_book_data=candidate,
                        field_map=isbndb_field_map,
                        list_fields=list_fields,
                        object_fields=object_fields
                    )
                    # Add standard metadata
                    extracted_data["Book_ID"] = book_id
                    extracted_data["DataSource"] = IsbnDbClient.PROVIDER_NAME
                    extracted_data["Fetched_Timestamp"] = fetch_timestamp
                    # Add match details if needed for analysis
                    extracted_data["Match_Details"] = details

                    matched_editions.append(extracted_data)
                except Exception as e:
                    logger.exception(f"Book ID '{book_id}', Candidate ISBN '{candidate_isbn13}': Error extracting data for matched edition.")

        return matched_editions

    def _check_match(
        self,
        norm_input_title: str,
        norm_input_author: str,
        candidate_title: Optional[str],
        candidate_authors_list: Optional[List[str]]
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Checks if a candidate book matches the input criteria based on settings.

        Args:
            norm_input_title: Normalized title from the input source.
            norm_input_author: Normalized primary author from the input source (surname preferred).
            candidate_title: Title from the API candidate.
            candidate_authors_list: List of authors from the API candidate.

        Returns:
            A tuple: (bool indicating match, dict containing match details/scores).
        """
        details = {"match_type": self.settings.matching_type}
        if not candidate_title or not candidate_authors_list:
            details["reason"] = "Missing candidate title or authors"
            return False, details

        norm_candidate_title = normalize_string(candidate_title)
        norm_candidate_authors = [normalize_string(a) for a in candidate_authors_list if a]

        if not norm_candidate_title or not norm_candidate_authors:
             details["reason"] = "Normalized candidate title or authors are empty"
             return False, details

        # --- Exact Matching ---
        if self.settings.matching_type == 'exact':
            title_match = norm_input_title == norm_candidate_title
            # Check if the normalized input author exists exactly in the normalized candidate list
            # Also handle surname check if input was "Surname, ..."
            author_match = any(norm_input_author == norm_cand_auth for norm_cand_auth in norm_candidate_authors) or \
                           any(norm_input_author in norm_cand_auth.split() for norm_cand_auth in norm_candidate_authors) # Simple check if surname is in candidate name parts


            details["title_match_exact"] = title_match
            details["author_match_exact"] = author_match
            return title_match and author_match, details

        # --- Fuzzy Matching ---
        elif self.settings.matching_type == 'fuzzy':
            # Title Score
            title_score = self.fuzzy_scorer_func(norm_input_title, norm_candidate_title)
            details["title_score"] = round(title_score)

            # Author Score - Find best match within the list
            best_author_score = 0
            if norm_candidate_authors:
                # Use process.extractOne for efficiency if scorer supports it,
                # otherwise loop manually
                try:
                    # extractOne returns (best_match, score, index)
                    best_match_info = process.extractOne(
                        norm_input_author,
                        norm_candidate_authors,
                        scorer=self.fuzzy_scorer_func,
                        score_cutoff=0 # Get score even if below threshold initially
                    )
                    if best_match_info:
                        best_author_score = best_match_info[1]
                        details["best_candidate_author"] = best_match_info[0]
                except Exception as e:
                     # Fallback to manual loop if extractOne fails or scorer is incompatible
                     logger.trace(f"extractOne failed for author matching (scorer: {self.fuzzy_scorer_func.__name__}), using loop. Error: {e}")
                     best_author_score = max(self.fuzzy_scorer_func(norm_input_author, norm_cand_auth)
                                             for norm_cand_auth in norm_candidate_authors)


            details["author_score"] = round(best_author_score)

            # Check against thresholds
            title_match = title_score >= self.settings.fuzzy_title_threshold
            author_match = best_author_score >= self.settings.fuzzy_author_threshold
            details["thresholds"] = f"T:{self.settings.fuzzy_title_threshold}/A:{self.settings.fuzzy_author_threshold}"

            return title_match and author_match, details

        else:
            # Should not happen if settings validation works, but handle defensively
            logger.error(f"Unknown matching_type: {self.settings.matching_type}")
            details["reason"] = "Unknown matching type"
            return False, details

    def _extract_edition_data(
        self,
        candidate_book_data: Dict[str, Any],
        field_map: Dict[str, str],
        list_fields: List[str],
        object_fields: List[str]
    ) -> Dict[str, Any]:
        """Extracts and formats data for a single matched edition."""
        extracted_data = {}
        for output_name, provider_field in field_map.items():
            raw_value = candidate_book_data.get(provider_field)

            # Handle special case for ISBN10 (might be in 'isbn' field)
            if output_name == "ISBN10" and raw_value is None:
                 raw_value = candidate_book_data.get("isbn")

            processed_value = None
            if raw_value is not None:
                if output_name in list_fields or output_name in object_fields:
                    try:
                        # Store lists/dicts as JSON strings
                        processed_value = json.dumps(raw_value)
                    except TypeError as e:
                        logger.warning(f"Could not JSON serialize field '{provider_field}' (value: {raw_value}): {e}")
                        processed_value = str(raw_value) # Fallback to string representation
                else:
                    # Ensure basic types are strings or numbers, handle potential issues
                    if isinstance(raw_value, (str, int, float, bool)):
                         processed_value = raw_value
                    else:
                         # Fallback for unexpected types
                         processed_value = str(raw_value)
            # else: keep processed_value as None if raw_value is None

            extracted_data[output_name] = processed_value

        return extracted_data