# Import the Pinecone library
from pinecone import Pinecone
from pythonConverterSplit import extraction
import time

# Initialize a Pinecone client with your API key
def upsertReport(inputFileName):
    pc = Pinecone(api_key="pcsk_6qzJGA_5xUfNgGmkyDar5tSg2gANqTCzPVWQjutiDaHyDDvFW8KEefuAxHvY1UmXJXJD4J")

    # Create a dense index with integrated embedding
    index_name = "aarontest"
    extractedResults = extraction(inputFileName)
    if extractedResults[1] == "Could not find ToC":
        return "Error"
    # Target the index
    dense_index = pc.Index(index_name)
    print("HELP ME")
    # Upsert the records into a namespace
    dense_index.upsert_records("example-namespace", extractedResults)

    # Wait for the upserted vectors to be indexed
    print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    time.sleep(10)

    # View stats for the index
    stats = dense_index.describe_index_stats()
    return str(stats)

