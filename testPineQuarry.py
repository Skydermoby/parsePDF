from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_6qzJGA_5xUfNgGmkyDar5tSg2gANqTCzPVWQjutiDaHyDDvFW8KEefuAxHvY1UmXJXJD4J")

index_list = pc.list_indexes()

print(index_list)

#host name: aarontest-x2rea8e.svc.aped-4627-b74a.pinecone.io

index = pc.Index(host="aarontest-x2rea8e.svc.aped-4627-b74a.pinecone.io")

results = index.search(
    namespace="example-namespace", 
    query={
        "inputs": {"text": "Disease prevention"}, 
        "top_k": 2
    },
    fields=["category", "chunk_text"]
)

print(results)