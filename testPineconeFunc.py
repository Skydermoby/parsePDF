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

    if len(extractedResults) > 90:
        bookmark = 0
        while bookmark < len(extractedResults):
            if bookmark + 90 > len(extractedResults):
                tempList = extractedResults[bookmark: len(extractedResults)]
            else:
                tempList = extractedResults[bookmark: bookmark + 90]
            dense_index.upsert_records("example-namespace", tempList)
            bookmark = bookmark + 90
    else:
        print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
        dense_index.upsert_records("example-namespace", extractedResults)

    # Wait for the upserted vectors to be indexed
    time.sleep(10)

    # View stats for the index
    stats = dense_index.describe_index_stats()
    return str(stats)

#print(upsertReport("Uploaded\\NCT00230607_SAP_001.pdf"))