import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def build_embeddings_index(products):
    """
    Builds a FAISS vector index from product text data.

    This function:
    - Combines relevant product fields into a single text string
    - Generates semantic embeddings using a sentence transformer model
    - Creates a FAISS index using inner product (cosine similarity)
    - Stores vectors in the index for fast similarity search

    The resulting index allows an AI agent to perform semantic searches,
    finding products that are similar in meaning even when the user's
    query does not exactly match the product text.

    Args:
        products (list): A list of product dictionaries. Each product is
                         expected to contain 'id', 'name', 'category',
                         'brand', and 'description'.

    Returns:
        tuple:
            - index (faiss.Index): The FAISS index containing product vectors
            - ids (list): A list mapping index positions to product IDs
    """
    texts = []
    ids = []

    for product in products:
        text = f"{product['name']} {product['category']} {product['brand']} {product['description']}"
        texts.append(text)
        ids.append(product['id'])

    vectors = model.encode(texts, normalize_embeddings=True)
    dim = vectors.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(np.array(vectors).astype('float32'))

    return index, ids