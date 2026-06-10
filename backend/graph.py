import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

_driver = None

def _get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            os.environ["NEO4J_URI"],
            auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
        )
    return _driver

def related_pages(start_url: str, hops: int = 2) -> list[str]:
    driver = _get_driver()
    query = (
        "MATCH (a:Page {url: $start})-[:LINKS_TO*1..%d]->(b:Page) "
        "RETURN DISTINCT b.url AS url LIMIT 10" % hops
    )
    with driver.session() as session:
        result = session.run(query, start=start_url)
        return [record["url"] for record in result]

if __name__ == "__main__":
    start = "https://fastapi.tiangolo.com/tutorial/security/"
    for url in related_pages(start):
        print(url)