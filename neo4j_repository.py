from dataclasses import dataclass
from pprint import pprint

from neo4j import GraphDatabase
import uuid
from typing import List, Dict, Any, Optional

@dataclass
class TArc:
    id: str
    label: str
    props: Dict[str, Any]
    node_uri_from: str
    node_uri_to: str

@dataclass
class TNode:
    id: str
    uri: str
    labels: List[str]
    props: Dict[str, Any]
    arcs: Optional[List[TArc]] = None


class Neo4jRepository:
    def __init__(self, uri: str, user: str, password: str) -> None:
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self) -> None:
        self.driver.close()

    def generate_random_string(self) -> str:
        return str(uuid.uuid4())

    def run_custom_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return [record.data() for record in result]

    def get_all_nodes(self) -> List[TNode]:
        query = "MATCH (n) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            return [self.collect_node(record["n"]) for record in result]

    def get_all_nodes_and_arcs(self) -> List[TNode]:
        query = """
        MATCH (n)-[r]->(m)
        RETURN n, r, m.uri as to_uri, type(r) as rel_type
        """

        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            nodes_dict = {}

            for record in result:
                node_data = record["n"]
                arc_data = record["r"]
                to_uri = record["to_uri"]
                rel_type = record["rel_type"]

                node_uri = node_data.get("uri")

                if node_uri not in nodes_dict:
                    nodes_dict[node_uri] = self.collect_node(node_data)
                    nodes_dict[node_uri].arcs = []

                arc = self.collect_arc(arc_data)
                arc.node_uri_from = node_uri
                arc.node_uri_to = to_uri
                arc.label = rel_type
                nodes_dict[node_uri].arcs.append(arc)

            return list(nodes_dict.values())

    def get_nodes_by_labels(self, labels: List[str]) -> List[TNode]:
        label_str = ":".join(labels)
        query = f"MATCH (n:{label_str}) RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            return [self.collect_node(record["n"]) for record in result]

    def get_node_by_uri(self, uri: str) -> Optional[TNode]:
        query = "MATCH (n {uri: $uri}) RETURN n"
        with self.driver.session() as session:
            record = session.run(query, {"uri": uri}).single()
            return self.collect_node(record["n"]) if record else None

    def create_node(self, params: Dict[str, Any], labels: Optional[List[str]] = None) -> TNode:
        if not params["uri"]:
            params["uri"] = self.generate_random_string()

        labels_str = ""
        if labels:
            labels_str = ":" + ":".join(params["labels"])

        query = f"""
        CREATE (n{labels_str} {{
            uri: $uri,
            title: $title,
            description: $description
        }})
        RETURN n
        """

        self.run_custom_query(query, params)

    def create_arc(self, node1_uri: str, node2_uri: str, rel_type: str = "RELATED") -> TArc:
        query = f"""
            MATCH (a {{uri: $node1_uri}}), (b {{uri: $node2_uri}})
            CREATE (a)-[r:{rel_type} {{id: randomUUID(), uri: $rel_type}}]->(b)
            RETURN r
        """
        with self.driver.session() as session:
            record = session.run(query, {
                "node1_uri": node1_uri,
                "node2_uri": node2_uri,
                "rel_type": rel_type
            }).single()
            return self.collect_arc(record["r"], node1_uri, node2_uri)

    def delete_node_by_uri(self, uri: str) -> None:
        query = "MATCH (n {uri: $uri}) DETACH DELETE n"
        with self.driver.session() as session:
            session.run(query, {"uri": uri})

    def delete_arc_by_id(self, arc_id: str) -> None:
        query = "MATCH ()-[r]->() WHERE r.id = $id DELETE r"
        with self.driver.session() as session:
            session.run(query, {"id": arc_id})

    def update_node(self, uri: str, params: Dict[str, Any]) -> Optional[TNode]:
        query = """
            MATCH (n {uri: $uri})
            SET n += $params
            RETURN n
        """
        with self.driver.session() as session:
            record = session.run(query, {"uri": uri, "params": params}).single()
            return self.collect_node(record["n"]) if record else None

    @staticmethod
    def collect_node(node_data) -> TNode:
        props = dict(node_data.items())

        return TNode(
            id=node_data.element_id,
            uri=props.get("uri", ""),
            labels=list(node_data.labels),
            props=props,
            arcs=None
        )

    @staticmethod
    def collect_arc(arc_data) -> TArc:
        props = dict(arc_data.items())

        return TArc(
            id=arc_data.element_id,
            label=arc_data.type,
            props=props,
            node_uri_from="",
            node_uri_to=""
        )


class Main:
    def __init__(self):
        self.repository = Neo4jRepository(
            uri="neo4j://127.0.0.1:7687",
            user="neo4j",
            password="12345678"
        )

    def simple_demo(self):
        node = self.repository.create_node({
            "title": "Тестовый узел",
            "description": "Это тестовый узел для демонстрации"
        })

        pprint(f"Создан узел: {node['title']}")
        pprint(f"URI узла: {node['uri']}")

        self.repository.close()


# Создание экземпляра и вызов функции
if __name__ == "__main__":
    app = Main()
    app.simple_demo()
