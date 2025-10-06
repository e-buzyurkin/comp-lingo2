from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
import json

from db.api.corpus_repository import CorpusRepository
from db.api.text_repository import TextRepository

# --- CORPUS ---

@api_view(['GET'])
def getCorpus(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponse(status=400)
    repo = CorpusRepository()
    result = repo.getCorpus(id)
    return Response(result)

@api_view(['POST'])
def createCorpus(request):
    data = json.loads(request.body.decode('utf-8'))
    repo = CorpusRepository()
    result = repo.create_corpus(data=data)
    return JsonResponse(result)

@api_view(['PUT'])
def updateCorpus(request, corpus_id):
    data = json.loads(request.body.decode('utf-8'))
    repo = CorpusRepository()
    result = repo.update_corpus(corpus_id, data)
    return JsonResponse(result)

@api_view(['DELETE'])
def deleteCorpus(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponse(status=400)
    repo = CorpusRepository()
    result = repo.deleteCorpus(id)
    return Response(result)


# --- TEXT ---

@api_view(['GET'])
def getText(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponse(status=400)
    repo = TextRepository()
    result = repo.getText(id)
    return Response(result)

@api_view(['POST'])
def createText(request):
    data = json.loads(request.body.decode('utf-8'))
    repo = TextRepository()
    result = repo.create_text(data=data)
    return JsonResponse(result)

@api_view(['PUT'])
def createText(request, text_id):
    data = json.loads(request.body.decode('utf-8'))
    repo = TextRepository()
    result = repo.update_text(text_id, data)
    return JsonResponse(result)

@api_view(['DELETE'])
def deleteText(request):
    id = request.GET.get('id')
    if not id:
        return HttpResponse(status=400)
    repo = TextRepository()
    result = repo.deleteText(id)
    return Response(result)
