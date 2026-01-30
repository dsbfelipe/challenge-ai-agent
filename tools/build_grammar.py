import re
from collections import Counter
from unidecode import unidecode

STOPWORDS = {
    "de", "para", "com", "sem", "e", "a", "o", "as", "os", "um", "uma", "ou", "do", "da", "no", "na"
}

def build_grammar(products):
    """
    Builds a simple word frequency dictionary from a list of products.

    This function:
    - Combines relevant product fields (name, category, brand, description)
    - Normalizes the text (lowercase and removes accents)
    - Extracts individual words using regex
    - Removes common stopwords
    - Counts how often each word appears

    The resulting dictionary can be used as a basic "grammar" or vocabulary
    to help an AI agent understand common terms in the product catalog,
    improving search, matching, or suggestion logic.

    Args:
        products (list): A list of product dictionaries. Each product is
                         expected to have the keys: 'name', 'category',
                         'brand', and 'description'.

    Returns:
        dict: A dictionary where keys are words and values are their
              frequency across all products.
    """
    counter = Counter()

    for product in products:
        text = f"{product['name']} {product['category']} {product['brand']} {product['description']}"
        text = unidecode(text.lower())

        words = re.findall(r'\b\w+\b', text)
        filtered_words = [word for word in words if word not in STOPWORDS]
        counter.update(filtered_words)

    return dict(counter)