# phantom_enrichment/utils/exceptions.py

class PhantomEnrichmentError(Exception):
    """Base exception class for the phantom-enrichment application."""
    pass

class ConfigurationError(PhantomEnrichmentError):
    """Exception raised for errors in configuration loading or validation."""
    pass

class DataSourceError(PhantomEnrichmentError):
    """Exception raised for errors related to reading or writing data sources."""
    pass

class EnrichmentError(PhantomEnrichmentError):
    """Exception raised during the enrichment process (e.g., API errors, matching failures)."""
    pass

class ProviderApiError(EnrichmentError):
    """Exception raised specifically for errors interacting with an external provider API."""
    def __init__(self, provider_name: str, message: str, status_code: int | None = None):
        self.provider_name = provider_name
        self.status_code = status_code
        full_message = f"[{provider_name} API Error]"
        if status_code:
            full_message += f" (Status: {status_code})"
        full_message += f": {message}"
        super().__init__(full_message)

class MatchingError(EnrichmentError):
    """Exception raised when a definitive match cannot be found."""
    pass