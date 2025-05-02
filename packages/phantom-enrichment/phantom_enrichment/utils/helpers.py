# phantom_enrichment/utils/helpers.py

import re
import unicodedata
from typing import Optional

def normalize_string(text: Optional[str]) -> str:
    """
    Normalizes a string for comparison:
    - Converts to lowercase.
    - Removes common punctuation.
    - Normalizes unicode characters (e.g., accents).
    - Collapses multiple whitespace characters.
    - Handles potential None input.

    Args:
        text: The input string or None.

    Returns:
        The normalized string, or an empty string if input was None.
    """
    if text is None:
        return ""

    # Normalize unicode characters (e.g., convert accented chars to base)
    # NFKD decomposes characters, then encode/decode removes combining marks
    try:
        text = unicodedata.normalize('NFKD', str(text))
        text = text.encode('ASCII', 'ignore').decode('ASCII')
    except Exception:
        # Fallback if complex unicode causes issues, just lowercase
         pass # Keep original text if normalization fails catastrophically

    # Convert to lowercase
    text = text.lower()

    # Remove common punctuation (keep spaces and alphanumeric)
    # Allows basic characters, removes most symbols
    text = re.sub(r'[^\w\s-]', '', text) # Keep word chars, whitespace, hyphens

    # Replace multiple whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def generate_book_id(title: Optional[str], author: Optional[str]) -> str:
    """
    Generates the standardized Book ID (B-TITLE|AUTHOR).

    Args:
        title: The book title from the input source.
        author: The book author from the input source.

    Returns:
        The generated Book ID string.
    """
    norm_title = re.sub(r'\s+', '', normalize_string(title)).upper()
    # Special handling for author: maybe take only first part if "Surname, Name"
    norm_author = normalize_string(author)
    # Simple split on comma for "Surname, Name" format
    if ',' in norm_author:
         norm_author = norm_author.split(',')[0].strip()
    norm_author = re.sub(r'\s+', '', norm_author).upper()

    return f"B-{norm_title}|{norm_author}"


if __name__ == '__main__':
    # Test cases
    print(f"'J R' -> '{normalize_string('J R')}'")
    print(f"'JR' -> '{normalize_string('JR')}'")
    print(f"'Austerlitz' -> '{normalize_string('Austerlitz')}'")
    print(f"'W.G. Sebald' -> '{normalize_string('W.G. Sebald')}'")
    print(f"'Sebald, W. G.' -> '{normalize_string('Sebald, W. G.')}'")
    print(f"'Café' -> '{normalize_string('Café')}'")
    print(f"'  Multiple   Spaces! ' -> '{normalize_string('  Multiple   Spaces! ')}'")
    print(f"None -> '{normalize_string(None)}'")

    print(f"Book ID for ' Austerlitz ', ' Sebald, W.G. ': '{generate_book_id(' Austerlitz ', ' Sebald, W.G. ')}'")
    print(f"Book ID for 'J R', 'Gaddis, William': '{generate_book_id('J R', 'Gaddis, William')}'")
    print(f"Book ID for 'JR', 'William Gaddis': '{generate_book_id('JR', 'William Gaddis')}'")