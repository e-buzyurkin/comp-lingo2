from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse, HttpResponse
import json

from db.api.neo4j_repository import Neo4jRepository
from db.api.ontology_repository import OntologyRepository

NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "12345678"


# ================== HELPER ==================

def get_repo():
    neo = Neo4jRepository(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    return OntologyRepository(neo)


# ================== ONTOLOGY ==================

@api_view(['GET'])
def get_ontology(request):
    repo = get_repo()
    ontology = repo.get_ontology()
    repo.repo.close()
    return JsonResponse(ontology.to_dict(), safe=False)


# ================== CLASS ==================

@api_view(['GET'])
def get_ontology_parent_classes(request):
    repo = get_repo()
    data = repo.get_ontology_parent_classes()
    repo.repo.close()
    return JsonResponse([c.to_dict() for c in data], safe=False)


@api_view(['GET'])
def get_class(request):
    uri = request.GET.get("uri")
    if not uri:
        return HttpResponse("Missing ?uri=", status=400)
    repo = get_repo()
    data = repo.get_class(uri)
    repo.repo.close()
    return JsonResponse(data.to_dict() if data else {}, safe=False)


@api_view(['GET'])
def get_class_parents(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    data = repo.get_class_parents(uri)
    repo.repo.close()
    return JsonResponse([d.to_dict() for d in data], safe=False)


@api_view(['GET'])
def get_class_children(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    data = repo.get_class_children(uri)
    repo.repo.close()
    return JsonResponse([d.to_dict() for d in data], safe=False)


@api_view(['GET'])
def get_class_objects(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    data = repo.get_class_objects(uri)
    repo.repo.close()
    return JsonResponse([d.to_dict() for d in data], safe=False)


@api_view(['POST'])
def create_class(request):
    data = json.loads(request.body)
    title = data.get("title")
    description = data.get("description", "")
    parent_uri = data.get("parent_uri")
    repo = get_repo()
    obj = repo.create_class(title, description, parent_uri)
    repo.repo.close()
    return JsonResponse(obj.to_dict(), safe=False)


@api_view(['PUT'])
def update_class(request):
    data = json.loads(request.body)
    uri = data.get("uri")
    params = data.get("params", {})
    repo = get_repo()
    obj = repo.update_class(uri, params)
    repo.repo.close()
    return JsonResponse(obj.to_dict() if obj else {}, safe=False)


@api_view(['DELETE'])
def delete_class(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    repo.delete_class(uri)
    repo.repo.close()
    return JsonResponse({"deleted": uri})


# ================== CLASS ATTRIBUTES ==================

@api_view(['POST'])
def add_class_attribute(request):
    data = json.loads(request.body)
    class_uri = data.get("class_uri")
    title = data.get("title")
    repo = get_repo()
    attr = repo.add_class_attribute(class_uri, title)
    repo.repo.close()
    return JsonResponse(attr.to_dict(), safe=False)


@api_view(['DELETE'])
def delete_class_attribute(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    repo.delete_class_attribute(uri)
    repo.repo.close()
    return JsonResponse({"deleted": uri})


@api_view(['POST'])
def add_class_object_attribute(request):
    data = json.loads(request.body)
    class_uri = data["class_uri"]
    attr_name = data["attr_name"]
    range_class_uri = data["range_class_uri"]
    repo = get_repo()
    obj = repo.add_class_object_attribute(class_uri, attr_name, range_class_uri)
    repo.repo.close()
    return JsonResponse(obj.to_dict(), safe=False)


@api_view(['DELETE'])
def delete_class_object_attribute(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    repo.delete_class_object_attribute(uri)
    repo.repo.close()
    return JsonResponse({"deleted": uri})


@api_view(['POST'])
def add_class_parent(request):
    data = json.loads(request.body)
    parent_uri = data["parent_uri"]
    target_uri = data["target_uri"]
    repo = get_repo()
    repo.add_class_parent(parent_uri, target_uri)
    repo.repo.close()
    return JsonResponse({"parent_added": parent_uri, "target": target_uri})


# ================== OBJECTS ==================

@api_view(['GET'])
def get_object(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    data = repo.get_object(uri)
    repo.repo.close()
    return JsonResponse(data.to_dict() if data else {}, safe=False)


@api_view(['POST'])
def create_object(request):
    data = json.loads(request.body)
    class_uri = data["class_uri"]
    params = data["params"]
    repo = get_repo()
    obj = repo.create_object(class_uri, params)
    repo.repo.close()
    return JsonResponse(obj, safe=False)


@api_view(['PUT'])
def update_object(request):
    data = json.loads(request.body)
    uri = data["uri"]
    params = data["params"]
    repo = get_repo()
    obj = repo.update_object(uri, params)
    repo.repo.close()
    return JsonResponse(obj.to_dict() if obj else {}, safe=False)


@api_view(['DELETE'])
def delete_object(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    repo.delete_object(uri)
    repo.repo.close()
    return JsonResponse({"deleted": uri})


# ================== CLASS SIGNATURE ==================

@api_view(['GET'])
def collect_signature(request):
    uri = request.GET.get("uri")
    repo = get_repo()
    sig = repo.collect_signature(uri)
    repo.repo.close()
    return JsonResponse(sig.to_dict() if sig else {}, safe=False)
