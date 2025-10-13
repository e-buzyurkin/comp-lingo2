from rest_framework.decorators import api_view
from django.http import JsonResponse
import numpy as np
from db.utils.embedding_utils import EmbeddingUtils


@api_view(["POST"])
def chunk_text(request):
    data = request.data
    text = data.get("text", "")
    utils = EmbeddingUtils()
    chunks = utils.get_chunks(text)
    return JsonResponse({"chunks": chunks})


@api_view(["POST"])
def generate_embeddings(request):
    data = request.data
    texts = data.get("texts", [])
    utils = EmbeddingUtils()
    embeddings = utils.get_embeddings(texts)
    return JsonResponse({"embeddings": embeddings.tolist()})


@api_view(["POST"])
def compare_embeddings(request):
    data = request.data
    emb1 = np.array(data.get("embedding1"))
    emb2 = np.array(data.get("embedding2"))

    utils = EmbeddingUtils()
    similarity = utils.cos_compare(emb1, emb2)
    return JsonResponse({"cosine_similarity": similarity})
