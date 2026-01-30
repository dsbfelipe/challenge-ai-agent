from rapidfuzz import process

def spellcheck(query: str, grammar: dict) -> str:
    """
    Performs basic spell correction on a search query using a known vocabulary.

    This function:
    - Splits the query into individual words
    - Compares each word against a vocabulary built from the product catalog
    - Uses fuzzy matching to find the closest known word
    - Replaces the word if the similarity score is high enough
    - Keeps the original word if no good match is found

    It helps handle typos and misspellings in user search queries,
    improving the chances of matching relevant products.

    Args:
        query (str): The original user search query.
        grammar (dict): A dictionary representing known words
                        (typically generated from the product catalog).

    Returns:
        str: The corrected query with misspelled words fixed when possible.
    """
    words = query.split()
    vocabulary = list(grammar.keys())
    corrected_words = []

    for word in words:
        match, score, _ = process.extractOne(word, vocabulary)
        if score >= 85:
            corrected_words.append(match)
        else:
            corrected_words.append(word)

    return ' '.join(corrected_words)