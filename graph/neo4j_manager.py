from neo4j import GraphDatabase
from config.settings import Settings


class Neo4jManager:

    def __init__(self):
        try:
            self.driver = GraphDatabase.driver(
                Settings.NEO4J_URI,
                auth=(Settings.NEO4J_USER, Settings.NEO4J_PASSWORD)
            )
        except Exception as e:
            raise RuntimeError(f"Neo4j connection failed: {str(e)}")

    def close(self):
        if self.driver:
            self.driver.close()

    def add_case(self, case_name):
        try:
            with self.driver.session() as session:
                session.run(
                    "MERGE (c:Case {name:$name})",
                    name=case_name
                )
        except Exception as e:
            print(f"Error adding case: {e}")

    def add_citation(self, from_case, to_case):
        try:
            with self.driver.session() as session:
                session.run("""
                    MERGE (a:Case {name:$from_case})
                    MERGE (b:Case {name:$to_case})
                    MERGE (a)-[:CITES]->(b)
                """,
                from_case=from_case,
                to_case=to_case
                )
        except Exception as e:
            print(f"Error adding citation: {e}")

    def get_centrality(self, case_name):
        """
        Returns simple in-degree centrality.
        You can later upgrade to PageRank.
        """
        try:
            with self.driver.session() as session:
                result = session.run("""
                    MATCH (c:Case {name:$name})
                    OPTIONAL MATCH (other:Case)-[:CITES]->(c)
                    RETURN count(other) as citation_count
                """, name=case_name)

                record = result.single()
                return record["citation_count"] if record else 0

        except Exception as e:
            print(f"Centrality error: {e}")
            return 0