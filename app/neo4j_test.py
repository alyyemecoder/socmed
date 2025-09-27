from neo4j import GraphDatabase

uri = "neo4j+s://a00e68dd.databases.neo4j.io"
user = "neo4j"
password = "LSDLXPhLwuSb7-mLdi5JEgaiVWzqKdvLeLhgPGHLpds"

driver = GraphDatabase.driver(uri, auth=(user, password))

try:
    with driver.session() as session:
        result = session.run("RETURN '✅ Connected to Neo4j Aura!' AS message")
        print(result.single()["message"])
except Exception as e:
    print("❌ Connection failed:", e)