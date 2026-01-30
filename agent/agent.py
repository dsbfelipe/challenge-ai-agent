from agent.prompt import PROMPT

from tools.normalize import normalize_text
from tools.spellcheck import spellcheck
from tools.semantic_search import semantic_search
from tools.suggest_alternatives import suggest_alternatives

import json


with open("vectorstore/grammar.json") as f:
    GRAMMAR = json.load(f)

def run_search(query: str):
    """
    Runs the e-commerce search pipeline.

    Steps:
    1️ - Normalize the query
    2️ - Apply spellcheck
    3️ - Perform semantic search
    4️ - If no results, generate an alternative suggestion with the model
    """
    normalized = normalize_text(query)
    corrected = spellcheck(normalized, GRAMMAR)
    results = semantic_search(corrected)

    if not results:
        alt_query = suggest_alternatives(query)
        return {
            "results": [],
            "alternative_suggestion": alt_query
        }
    
    return results