from typing import Dict, Any

from .entities import *
from .neo4j_repository import Neo4jRepository


class OntologyRepository:
    def __init__(self, repository: Neo4jRepository):
        self.repo = repository

    # ==================== CLASS ====================

    def get_ontology(self) -> Ontology:
        all_nodes = self.repo.get_all_nodes()

        classes = [collect_from_node(node) for node in all_nodes if "Class" in node.labels]
        objects = [collect_from_node(obj) for obj in all_nodes if "Object" in obj.labels]

        return Ontology(classes, objects)


    def get_ontology_parent_classes(self) -> List[Class]:
        query = """
        MATCH (c:Class)
        WHERE NOT (c)<-[:SUBCLASS_OF]-(:Class)
        RETURN c, labels(c) as class_labels
        """


        results = self.repo.run_custom_query(query)
        classes = []

        for result in results:
            node_data = result["c"]
            class_label = result.get("class_labels", [])

            node_data["labels"] = class_label
            class_obj = collect_from_node(node_data)
            classes.append(class_obj)

        return classes

    def get_class(self, class_uri: str) -> Optional[Class]:
        node = self.repo.get_node_by_uri(class_uri)

        if node is None or "Class" not in node.labels:
            return None

        return collect_from_node(node)



    def get_class_parents(self, class_uri: str) -> List[Class]:
        query = """
        MATCH (c:Class {uri: $uri})-[:SUBCLASS_OF]->(parent:Class)
        RETURN parent, labels(parent) as parent_labels
        """
        results = self.repo.run_custom_query(query, {"uri": class_uri})
        parents = []

        for result in results:
            parent_data = result["parent"]
            parent_labels = result.get("parent_labels", [])

            parent_data["labels"] = parent_labels

            parent_class = collect_from_node(parent_data)
            parents.append(parent_class)

        return parents

    def get_class_children(self, class_uri: str) -> List[Class]:
        query = """
        MATCH (c:Class {uri: $uri})<-[:SUBCLASS_OF]-(child:Class)
        RETURN child
        """
        results = self.repo.run_custom_query(query, {"uri": class_uri})
        children = []

        for result in results:
            child_data = result["child"]
            child_labels = result.get("child_labels", [])

            # Добавляем метки к данным дочернего класса
            child_data["labels"] = child_labels

            child_class = collect_from_node(child_data)
            children.append(child_class)

        return children

    def get_class_objects(self, class_uri: str) -> List[Object]:
        query = """
        MATCH (o:Object)-[:rdf__type]->(c:Class {uri: $uri})
        RETURN o, labels(o) as object_labels
        """

        results = self.repo.run_custom_query(query, {"uri": class_uri})
        objects = []

        for result in results:
            object_data = result["o"]
            object_labels = result.get("object_labels", [])

            object_data["labels"] = object_labels

            obj = collect_from_node(object_data)
            objects.append(obj)

        return objects

    def update_class(self, class_uri: str, params: Dict[str, Any]) -> Optional[Class]:
        return collect_from_node(self.repo.update_node(class_uri, params))

    def create_class(self, title: str, description: str, parent_uri: Optional[str] = None) -> Class:
        uri = self.repo.generate_random_string()
        node = self.repo.create_node(
            {"uri": uri, "title": title, "description": description},
            labels=["Class", uri]
        )
        if parent_uri:
            self.repo.create_arc(node.uri, parent_uri, "SUBCLASS_OF")

        return collect_from_node(node)

    def delete_class(self, class_uri: str) -> None:
        query = """
        MATCH (c:Class {uri: $uri})
        OPTIONAL MATCH (c)<-[:SUBCLASS_OF*]-(child:Class)
        OPTIONAL MATCH (c)<-[:rdf__type*]-(o:Object)
        OPTIONAL MATCH (c)<-[:domain]-(q)
        DETACH DELETE c, child, o, q
        """
        self.repo.run_custom_query(query, {"uri": class_uri})

    # ==================== CLASS ATTRIBUTES ====================

    def add_class_attribute(self, class_uri: str, title: str) -> DatatypeProperty:
        prop = self.repo.create_node({"title": title}, labels=["DatatypeProperty"])

        self.repo.create_arc(prop.uri, class_uri, "domain")
        return collect_from_node(prop)

    def delete_class_attribute(self, prop_uri: str) -> None:
        self.repo.delete_node_by_uri(prop_uri)

    def add_class_object_attribute(self, class_uri: str, attr_name: str, range_class_uri: str) -> ObjectProperty:
        prop = self.repo.create_node({"title": attr_name}, labels=["ObjectProperty"])

        self.repo.create_arc(prop.uri, class_uri, "domain")
        self.repo.create_arc(prop.uri, range_class_uri, "range")

        return collect_from_node(prop)

    def delete_class_object_attribute(self, object_property_uri: str) -> None:
        self.repo.delete_node_by_uri(object_property_uri)

    def add_class_parent(self, parent_uri: str, target_uri: str) -> None:
        self.repo.create_arc(target_uri, parent_uri, "SUBCLASS_OF")

    # ==================== OBJECTS ====================

    def get_object(self, object_uri: str) -> Optional[Object]:
        node = self.repo.get_node_by_uri(object_uri)
        if node is None or "Object" not in node.labels:
            return None

        return collect_from_node(node)

    def delete_object(self, object_uri: str) -> None:
        self.repo.delete_node_by_uri(object_uri)

    def create_object(self, params: Dict[str, Any], obj_params: list[Dict[str, Any]]) -> Object:
        obj = self.repo.create_node(params, labels=["Object", params["uri"]])
        for param in obj_params:
            if param["direction"] == 1:
                self.repo.create_arc(obj.uri, param["value_uri"], param["rel_type"])
            else:
                self.repo.create_arc(param["value_uri"], obj.uri, param["rel_type"])


        return collect_from_node(obj)

    def update_object(self, object_uri: str, params: Dict[str, Any]) -> Optional[Object]:
        update_params = {"uri": params["uri"], "title": params["title"], "description": params["description"]}
        return self.repo.update_node(object_uri, update_params)

        # if params["datatype"]:
        #     for prop_name, value in params["datatype"].items():
        #         query = """
        #         MATCH (o:Object {uri: $object_uri})
        #         MERGE (o)-[r:HAS_VALUE {property: $prop_name}]->(v:Value {value: $value})
        #         """
        #         self.repo.run_custom_query(query, {
        #             "object_uri": object_uri,
        #             "prop_name": prop_name,
        #             "value": value
        #         })
        #
        # if params["properties"]:
        #     for prop_name, target_uri in params["properties"].items():
        #         query = """
        #         MATCH (o:Object {uri: $object_uri}), (target:Object {uri: $target_uri})
        #         MERGE (o)-[r]->(target)
        #         SET r.type = $prop_name
        #         """
        #         self.repo.run_custom_query(query, {
        #             "object_uri": object_uri,
        #             "target_uri": target_uri,
        #             "prop_name": prop_name
        #         })


    def collect_signature(self, class_uri: str) -> Optional[ClassSignature]:
        datatype_query = """
        MATCH (c:Class {uri: $class_uri})-[:domain]->(dtp:DatatypeProperty)
        RETURN dtp
        """
        datatype_results = self.repo.run_custom_query(datatype_query, {"class_uri": class_uri})

        datatype_properties = []
        for result in datatype_results:
            dtp_data = result["dtp"]
            datatype_properties.append(DatatypeProperty(
                    uri=dtp_data["uri"],
                    title=dtp_data["title"],
                    class_uri=class_uri
                )
            )


        object_query = """
        MATCH (c:Class {uri: $class_uri})-[:domain]->(op:ObjectProperty)-[:range]->(rng:Class)
        RETURN op, rng.uri as range_uri
        """
        object_results = self.repo.run_custom_query(object_query, {"class_uri": class_uri})

        object_properties = []
        for result in object_results:
            op_data = result["op"]
            object_properties.append(ObjectProperty(
                    uri=op_data["uri"],
                    title=op_data["title"],
                    class_uri=class_uri,
                    range_class_uri=result["range_uri"]
                )
            )

        return ClassSignature(
            class_uri=class_uri,
            datatype_properties=datatype_properties,
            object_properties=object_properties
        )