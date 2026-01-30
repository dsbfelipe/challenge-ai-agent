from data.products import PRODUCTS
from tools.build_grammar import build_grammar
from tools.build_index import build_embeddings_index

import faiss
import json

grammar = build_grammar(PRODUCTS)

with open("vectorstore/grammar.json", "w") as f:
    json.dump(grammar, f, ensure_ascii=False, indent=4)

index, ids = build_embeddings_index(PRODUCTS)
faiss.write_index(index, "vectorstore/index.faiss")

with open("vectorstore/product_ids.json", "w") as f:
    json.dump(ids, f, ensure_ascii=False, indent=4)

print("Successfully built and saved grammar and FAISS index.")