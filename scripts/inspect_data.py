import json, csv

docs = [json.loads(l) for l in open("data/documents.jsonl", encoding="utf-8")]
chunks = [json.loads(l) for l in open("data/chunks.jsonl", encoding="utf-8")]
with open("data/graph_edges.csv", encoding="utf-8") as f:
    edges = list(csv.DictReader(f))

doc_ids = {d["id"] for d in docs}
doc_urls = {d["url"] for d in docs}

print(f"docs={len(docs)}  chunks={len(chunks)}  edges={len(edges)}")
print("orphan chunks:", sum(1 for c in chunks if c["doc_id"] not in doc_ids))
print("dangling edges:", sum(1 for e in edges if e["target"] not in doc_urls))
print("avg chunks/doc:", round(len(chunks) / len(docs), 1))