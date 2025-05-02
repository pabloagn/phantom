# phantom_enrichment/enrichment/providers/isbndb_client.py

import requests
import time
import json
from urllib.parse import quote, urljoin
from loguru import logger
from typing import Dict, Any, Optional

# Assuming exceptions are defined in the utils module based on previous setup
from phantom_enrichment.utils.exceptions import ProviderApiError, ConfigurationError

class IsbnDbClient:
    """
    Client for interacting with the ISBNDB v2 REST API.

    Handles authentication, rate limiting, request execution, and error handling.
    """
    PROVIDER_NAME = "ISBNDB"
    # Standard rate limit is 1 req/sec. Add buffer. Premium/Pro could adjust this.
    DEFAULT_RATE_LIMIT_DELAY = 1.1 # seconds

    def __init__(self, api_key: str, base_url: str, rate_limit_delay: Optional[float] = None):
        """
        Initializes the ISBNDB client.

        Args:
            api_key: The ISBNDB REST API key.
            base_url: The base URL for the ISBNDB API (e.g., "https://api2.isbndb.com").
            rate_limit_delay: Optional override for the delay between requests (in seconds).
                              Defaults to DEFAULT_RATE_LIMIT_DELAY.
        """
        if not api_key:
            raise ConfigurationError(f"{self.PROVIDER_NAME}: API key is required.")
        if not base_url:
            raise ConfigurationError(f"{self.PROVIDER_NAME}: Base URL is required.")

        self.api_key = api_key
        # Ensure base URL doesn't have a trailing slash for urljoin to work correctly
        self.base_url = base_url.rstrip('/') + '/'
        self.rate_limit_delay = rate_limit_delay if rate_limit_delay is not None else self.DEFAULT_RATE_LIMIT_DELAY

        # Use a session object for connection pooling and persistent headers
        self.session = requests.Session()
        self.session.headers.update(self._get_headers())

        logger.info(f"{self.PROVIDER_NAME} client initialized. Base URL: {self.base_url}, Rate Limit Delay: {self.rate_limit_delay}s")

    def _get_headers(self) -> Dict[str, str]:
        """Returns the required authentication headers."""
        return {
            "Authorization": self.api_key,
            "Accept": "application/json",
            # Content-Type needed for POST requests, but doesn't hurt for GET
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None, data: Optional[Any] = None) -> Dict[str, Any]:
        """
        Makes an HTTP request to the ISBNDB API, handling rate limiting and errors.

        Args:
            method: HTTP method (e.g., "GET", "POST").
            endpoint: API endpoint path (e.g., "/books/query", "/book/isbn").
            params: Dictionary of URL query parameters.
            data: Request body data (for POST/PUT). Typically JSON string or dict.

        Returns:
            The parsed JSON response dictionary.

        Raises:
            ProviderApiError: If the API returns an error or the request fails.
        """
        # Ensure endpoint doesn't start with '/' if base_url already ends with '/'
        relative_endpoint = endpoint.lstrip('/')
        full_url = urljoin(self.base_url, relative_endpoint)

        # --- Rate Limiting ---
        logger.trace(f"Sleeping for {self.rate_limit_delay}s before API call.")
        time.sleep(self.rate_limit_delay)

        logger.debug(f"Making {self.PROVIDER_NAME} request: {method} {full_url}")
        if params:
            logger.trace(f"Request Params: {params}")
        if data:
             # Avoid logging potentially large data bodies at debug level unless needed
            logger.trace(f"Request Data Type: {type(data)}")

        try:
            response = self.session.request(
                method=method,
                url=full_url,
                params=params,
                json=data if method.upper() in ['POST', 'PUT'] and isinstance(data, dict) else None,
                data=data if method.upper() in ['POST', 'PUT'] and isinstance(data, str) else None,
                timeout=30 # Set a reasonable timeout (e.g., 30 seconds)
            )
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            try:
                # Try to parse error details from JSON response
                error_details = e.response.json()
                error_message = error_details.get('errorMessage', e.response.text) # Use errorMessage if present
                logger.error(f"{self.PROVIDER_NAME} HTTP Error {status_code} for {method} {full_url}. Response: {error_details}")
            except json.JSONDecodeError:
                # If response is not JSON
                error_message = e.response.text
                logger.error(f"{self.PROVIDER_NAME} HTTP Error {status_code} for {method} {full_url}. Response (non-JSON): {error_message}")

            raise ProviderApiError(
                provider_name=self.PROVIDER_NAME,
                message=f"HTTP Error {status_code}: {error_message}",
                status_code=status_code
            ) from e

        except requests.exceptions.Timeout:
            logger.error(f"{self.PROVIDER_NAME} request timed out for {method} {full_url}")
            raise ProviderApiError(provider_name=self.PROVIDER_NAME, message="Request timed out")

        except requests.exceptions.ConnectionError as e:
            logger.error(f"{self.PROVIDER_NAME} connection error for {method} {full_url}: {e}")
            raise ProviderApiError(provider_name=self.PROVIDER_NAME, message=f"Connection error: {e}")

        except requests.exceptions.RequestException as e:
            # Catch other potential requests library errors
            logger.error(f"{self.PROVIDER_NAME} request failed for {method} {full_url}: {e}")
            raise ProviderApiError(provider_name=self.PROVIDER_NAME, message=f"Request failed: {e}")

        # If the request was successful (status code 2xx)
        try:
            response_json = response.json()
            logger.debug(f"{self.PROVIDER_NAME} request successful ({response.status_code}) for {method} {full_url}")
            # logger.trace(f"Response JSON: {response_json}") # Be careful logging full response if large
            return response_json
        except json.JSONDecodeError as e:
            logger.error(f"{self.PROVIDER_NAME} failed to decode JSON response from {method} {full_url}. Status: {response.status_code}, Response: {response.text}")
            raise ProviderApiError(
                provider_name=self.PROVIDER_NAME,
                message=f"Invalid JSON response received (Status: {response.status_code})",
                status_code=response.status_code
            ) from e

    def search_books(self, query: str, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        Searches for books using the GET /books/{query} endpoint.

        Args:
            query: The search query string (e.g., "Title Author").
            page: The page number to retrieve (1-based).
            page_size: The number of results per page (max 100 for bulk).

        Returns:
            The parsed JSON response dictionary from the API.

        Raises:
            ProviderApiError: If the API request fails.
            ValueError: If page or page_size are invalid.
        """
        if page < 1:
            raise ValueError("Page number must be 1 or greater.")
        if not (1 <= page_size <= 100):
             # Note: Free tier might have lower practical limits, but API doc implies 100 max for bulk
             raise ValueError("Page size must be between 1 and 100.")

        if not query:
            logger.warning("Attempting ISBNDB search with an empty query.")
            # Depending on API behavior, might return error or empty result set.
            # Let the API handle it for now, but log warning.

        encoded_query = quote(query)
        endpoint = f"/books/{encoded_query}"
        params = {'page': page, 'pageSize': page_size}

        logger.info(f"Searching {self.PROVIDER_NAME} for query='{query}', page={page}, pageSize={page_size}")
        return self._make_request('GET', endpoint, params=params)

    def get_book_by_isbn(self, isbn: str) -> Dict[str, Any]:
        """
        Retrieves book details using the GET /book/{isbn} endpoint.

        Args:
            isbn: The ISBN (10 or 13) of the book.

        Returns:
            The parsed JSON response dictionary containing book details,
            or potentially an error structure if not found.

        Raises:
            ProviderApiError: If the API request fails.
        """
        if not isbn:
             raise ValueError("ISBN cannot be empty.")

        # Basic validation (length) - could be more sophisticated
        isbn = isbn.replace('-', '').replace(' ', '')
        if not (len(isbn) == 10 or len(isbn) == 13) or not isbn.isdigit():
             # Allow ISBNdb API to handle final validation, but log potential issue
             logger.warning(f"Provided ISBN '{isbn}' has unusual format. Proceeding anyway.")

        endpoint = f"/book/{isbn}"
        logger.info(f"Fetching book details from {self.PROVIDER_NAME} for ISBN: {isbn}")
        # A 404 here is a valid outcome (book not found), the caller should handle it.
        return self._make_request('GET', endpoint)

    # Potential future method for POST /books endpoint (bulk ISBN lookup)
    # def get_books_by_isbns_bulk(self, isbns: list[str]) -> Dict[str, Any]:
    #     """Retrieves multiple books using the POST /books endpoint."""
    #     if not isbns:
    #         return {"books": []} # Or handle as appropriate
    #
    #     endpoint = "/books"
    #     # The docs show data format 'isbns=isbn1,isbn2,...'
    #     # This is unusual for a JSON POST, usually expects a JSON body like {"isbns": ["...", "..."]}
    #     # Double-check the docs/examples carefully. Let's assume the string format for now.
    #     data_string = 'isbns=' + ','.join(isbns)
    #     logger.info(f"Fetching bulk book details from {self.PROVIDER_NAME} for {len(isbns)} ISBNs.")
    #     # Need to ensure _make_request handles string data correctly for POST if not sending JSON
    #     return self._make_request('POST', endpoint, data=data_string)

if __name__ == "__main__":
    import sys
    from dotenv import load_dotenv
    from pathlib import Path
    import os
    # --- Import logger explicitly if not already done via other imports ---
    from loguru import logger # Make sure logger is available
    # --- Need ProviderApiError and ConfigurationError for exception handling ---
    from phantom_enrichment.utils.exceptions import ProviderApiError, ConfigurationError


    # --- Function to find project root (copied/adapted from settings.py) ---
    def find_project_root_for_test(marker_files=(".env", "pyproject.toml")):
        """Finds the project root directory by searching upwards from this script's location."""
        current_dir = Path(__file__).resolve().parent # Start from this script's dir
        for directory in [current_dir] + list(current_dir.parents):
            for marker in marker_files:
                if (directory / marker).exists():
                    return directory
        # Fallback: If not found upwards, maybe CWD is the root? (Less reliable)
        cwd = Path.cwd()
        for marker in marker_files:
             if (cwd / marker).exists():
                  logger.warning(f"Could not find marker upwards from script, using CWD as root: {cwd}")
                  return cwd
        raise FileNotFoundError(f"Could not determine project root directory. Looked for {marker_files} starting from {current_dir}.")
    # --- End of function ---

    try:
        # --- Use the function to find the root ---
        project_root = find_project_root_for_test()
        dotenv_path = project_root / '.env'
    except FileNotFoundError as e:
        logger.error(f"Could not find project root: {e}. Cannot load .env.")
        sys.exit(1) # Exit if root not found


    logger.debug(f"Running test block in {__file__}")
    logger.debug(f"Calculated project root: {project_root}")
    logger.debug(f"Looking for .env file at: {dotenv_path}")

    # Load .env using override=True
    loaded = load_dotenv(dotenv_path=dotenv_path, override=True)

    if loaded:
        logger.debug(f".env file loaded successfully from {dotenv_path}")
    else:
        logger.warning(f".env file NOT loaded from {dotenv_path} (might not exist or is empty)")

    API_KEY = os.getenv("ISBNDB_API_KEY")
    BASE_URL = os.getenv("ISBNDB_BASE_URL", "https://api2.isbndb.com")

    # --- Add minimal logger setup just for this test block if main config fails ---
    # This ensures errors before client init are still logged somewhere
    if not logger: # Check if logger was somehow not configured
         logger.add(sys.stderr, level="DEBUG")
         logger.warning("Main logger config might have failed, using basic stderr logger for test.")

    if not API_KEY:
        # Using logger now should be safer
        logger.error(f"ISBNDB_API_KEY not found in environment variables after attempting to load {dotenv_path}. Cannot run test.")
        if dotenv_path.exists():
             logger.error(f"Hint: The file {dotenv_path} exists. Check if ISBNDB_API_KEY is defined correctly inside it.")
        else:
             logger.error(f"Hint: The file {dotenv_path} does not exist.")
        sys.exit(1) # Exit cleanly
    else:
        # Client initialization and test calls
        try:
            client = IsbnDbClient(api_key=API_KEY, base_url=BASE_URL)
            # ... (The actual test calls: Test 1, Test 2, Test 3 remain the same) ...

            # --- Test 1: Search ---
            logger.info("\n--- Testing Book Search ---")
            search_query = "Designing Data-Intensive Applications"
            try:
                results = client.search_books(search_query, page_size=5)
                logger.info(f"Search results for '{search_query}':")
                logger.info(f"\n{json.dumps(results, indent=2)}") # Log the JSON directly
                total_found = results.get('total')
                if total_found is not None:
                     logger.info(f"Total found: {total_found}")
                if total_found and total_found > 5:
                     # Test pagination
                     logger.info("\n--- Testing Pagination (Page 2) ---")
                     results_p2 = client.search_books(search_query, page=2, page_size=5)
                     logger.info(f"Search results for '{search_query}' (Page 2):")
                     logger.info(f"\n{json.dumps(results_p2, indent=2)}")

            except ProviderApiError as e:
                logger.error(f"Search failed: {e}")
            except ValueError as e:
                logger.error(f"Input validation error during search: {e}")


            # --- Test 2: Get by ISBN ---
            logger.info("\n--- Testing Get Book by ISBN ---")
            test_isbn = "9781449373320"
            try:
                book_details = client.get_book_by_isbn(test_isbn)
                logger.info(f"Details for ISBN {test_isbn}:")
                logger.info(f"\n{json.dumps(book_details, indent=2)}")
            except ProviderApiError as e:
                 logger.error(f"Get by ISBN failed: {e}")
                 if e.status_code == 404:
                      logger.warning(f"ISBN {test_isbn} might not exist in ISBNDB.")
            except ValueError as e:
                logger.error(f"Input validation error during get by ISBN: {e}")

             # --- Test 3: Get non-existent ISBN ---
            logger.info("\n--- Testing Get Non-Existent ISBN ---")
            test_isbn_bad = "0000000000"
            try:
                book_details_bad = client.get_book_by_isbn(test_isbn_bad)
                logger.info(f"Details for ISBN {test_isbn_bad}: {book_details_bad}")
            except ProviderApiError as e:
                 logger.error(f"Get by ISBN failed as expected for {test_isbn_bad}: {e}")
                 if e.status_code == 404:
                      logger.success(f"Received 404 Not Found for non-existent ISBN {test_isbn_bad}, as expected.")

        except ConfigurationError as e:
             logger.error(f"Client Initialization failed: {e}")
        except Exception as e:
             logger.exception(f"An unexpected error occurred during testing:") # logger.exception includes traceback