# Import the Pinecone library
from pinecone import Pinecone
from pythonConverterSplit import extraction
import time

# Initialize a Pinecone client with your API key
pc = Pinecone(api_key="pcsk_6qzJGA_5xUfNgGmkyDar5tSg2gANqTCzPVWQjutiDaHyDDvFW8KEefuAxHvY1UmXJXJD4J")

# Create a dense index with integrated embedding
index_name = "aarontest"
if not pc.has_index(index_name):
    pc.create_index_for_model(
        name=index_name,
        cloud="aws",
        region="us-east-1",
        embed={
            "model":"llama-text-embed-v2",
            "field_map":{"text": "chunk_text"}
        }
    )

inputFileName = "NCT00658021_SAP_001"
extractedResults = extraction(inputFileName)

# Target the index
dense_index = pc.Index(index_name)

# Upsert the records into a namespace
dense_index.upsert_records("example-namespace", extractedResults)

# Wait for the upserted vectors to be indexed

time.sleep(10)

# View stats for the index
stats = dense_index.describe_index_stats()
print(stats)

