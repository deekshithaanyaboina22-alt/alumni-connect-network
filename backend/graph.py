import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USER = os.getenv("COGNODB_USER")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'CognoDB Connected' AS message")
        return result.single()["message"]