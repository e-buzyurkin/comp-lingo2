# file: entities.py
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

from neo4j_repository import TNode


@dataclass
class Class:
    uri: str
    title: str
    description: Optional[str] = None
    labels: Optional[List[str]] = None


@dataclass
class Object:
    uri: str
    title: str
    class_uri: str
    description: Optional[str] = None


@dataclass
class Ontology:
    classes: List[Class]
    objects: List[Object]


@dataclass
class DatatypeProperty:
    uri: str
    title: str
    class_uri: str = None


@dataclass
class ObjectProperty:
    uri: str
    title: str
    class_uri: str = None
    range_class_uri: str = None


@dataclass
class ClassSignature:
    class_uri: str
    datatype_properties: List[DatatypeProperty]
    object_properties: List[ObjectProperty]


@dataclass
class Ontology:
    signatures: List[ClassSignature]
    objects: List[Object]


def collect_from_node(node: TNode) -> Optional[Class | Object | DatatypeProperty | ObjectProperty]:
    if node is None or node.props.get("uri") is None or node.props.get("title") is None:
        return None

    uri = node.props.get("uri")
    title = node.props.get("title")

    if node.labels.count("Class"):
        return Class(uri, title, node.props.get("description"))
    elif node.labels.count("Object"):
        return Object(uri, title, node.props.get("description"))
    elif node.labels.count("DatatypeProperty"):
        return DatatypeProperty(uri, title)
    elif node.labels.count("ObjectProperty"):
        return ObjectProperty(uri, title)
    else:
        return None
