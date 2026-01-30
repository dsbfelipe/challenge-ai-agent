import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from data.products import PRODUCTS

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
index = faiss.read_index("vectorstore/index.faiss")

with open("vectorstore/product_ids.json") as f:
    product_ids = json.load(f)

products_by_id = {p["id"]: p for p in PRODUCTS}

def semantic_search(query: str, k=5, min_score=0.5):
    vector = model.encode([query], normalize_embeddings=True)
    max_k = min(k, index.ntotal)

    scores, indices = index.search(
        np.array(vector).astype("float32"), max_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx == -1 or score < min_score:
            continue

        product_id = product_ids[idx]
        product = products_by_id.get(product_id)

        if not product:
            continue

        results.append({
            "product_id": product_id,
            "name": product["name"],
            "category": product["category"],
            "brand": product["brand"],
            "score": round(float(score), 4)
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results