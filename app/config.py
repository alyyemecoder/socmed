# app/config.py
import os
from dotenv import load_dotenv
from neomodel import config as neomodel_config

load_dotenv()

NEO4J_BOLT_URL = os.getenv("NEO4J_BOLT_URL", "neo4j+s://7f87ffb9.databases.neo4j.io") 
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# neomodel expects: bolt://username:password@host:port OR bolt://host:port with auth tuple
NEOMODEL_URL = f"bolt://{NEO4J_USER}:{NEO4J_PASSWORD}@{NEO4J_BOLT_URL.split('://')[-1]}"

# Set neomodel config
neomodel_config.DATABASE_URL = NEOMODEL_URL
