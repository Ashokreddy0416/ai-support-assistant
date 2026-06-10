import os, csv
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()
driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
)

with open("data/graph_edges.csv", encoding="utf-8") as f:
    edges = list(csv.DictReader(f))

def load(tx, src, tgt):
    tx.run(
        "MERGE (a:Page {url: $src}) "
        "MERGE (b:Page {url: $tgt}) "
        "MERGE (a)-[:LINKS_TO]->(b)",
        src=src, tgt=tgt,
    )

with driver.session() as session:
    for e in edges:
        session.execute_write(load, e["source"], e["target"])

print(f"Loaded {len(edges)} edges into Neo4j")
driver.close()