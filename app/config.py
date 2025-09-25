# app/config.py

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables from .env
load_dotenv()

# Retrieve credentials
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://a00e68dd.databases.neo4j.io")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "LSDLXPhLwuSb7-mLdi5JEgaiVWzqKdvLeLhgPGHLpds")

# Create Neo4j driver
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# Optional: test connection
def test_connection():
    try:
        with driver.session() as session:
            result = session.run("RETURN '✅ Neo4j Aura connection successful!' AS message")
            print(result.single()["message"])
    except Exception as e:
        print(f"❌ Connection failed: {e}")

# Run test on import
test_connection()