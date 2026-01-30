from unidecode import unidecode

def normalize_text(text: str) -> str:
    """
    Normalizes a text to make searches and comparisons easier.

    This function:
    - Converts the text to lowercase
    - Removes leading and trailing spaces
    - Removes accents and special characters (e.g. "ç", "ã", "é")

    It is useful in search scenarios (such as e-commerce search bars),
    where users may type words with spelling mistakes or different
    accent variations, allowing more consistent text comparison.

    Example:
        "Café com Leite " -> "cafe com leite"
    """
    return unidecode(text.lower().strip())