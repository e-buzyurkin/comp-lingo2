import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class EmbeddingUtils:
    def __init__(self):
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

    def get_chunks(self, texts: Union[str, List[str]], max_chunk_size: int = 500) -> List[str]:
        if isinstance(texts, str):
            texts = [texts]

        chunks = []
        for text in texts:
            text = text.strip()
            for i in range(0, len(text), max_chunk_size):
                chunk = text[i:i + max_chunk_size].strip()
                if chunk:
                    chunks.append(chunk)
        return chunks

    def get_embeddings(self, texts: Union[str, List[str]]) -> np.ndarray:
        if isinstance(texts, str):
            texts = [texts]
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings

    def cos_compare(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        emb1 = emb1.reshape(1, -1)
        emb2 = emb2.reshape(1, -1)
        return float(cosine_similarity(emb1, emb2)[0][0])
