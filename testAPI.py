from fastapi import FastAPI, File, UploadFile
from converter import extraction
import os
from pinecone import Pinecone
import shutil
from testPineconeFunc import upsertReport
from fastapi.middleware.cors import CORSMiddleware

#host name: aarontest-x2rea8e.svc.aped-4627-b74a.pinecone.io
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file recieved"}
    else:
        outputFile = "Uploaded\\" + file.filename
        if os.path.exists(outputFile):
            os.remove(outputFile)
        
        with open(outputFile, "wb") as f:
            f.write(file.file.read())
        #shutil.copyfileobj(file.file, outputFile)
        return file.filename
    


@app.get("/items/{item_id}")
async def get_item(item_id: str | None = None):
    print(len(item_id))
    filteredName = item_id[1:len(item_id)-1:1]
    filePath = "Uploaded\\"+filteredName
    if os.path.exists(filePath):
        return extraction(filePath)
        return "Item Found!"
    else: 
        return "Error: couldn't find file in storage" , filePath
    item = {"item_id": item_id}
    
    return item

@app.get("/pineconeUplpoad/{item_id}")
async def get_item(item_id: str | None = None):
    filteredName = item_id[1:len(item_id)-1:1]
    filePath = "Uploaded\\"+filteredName
    if os.path.exists(filePath):
        return upsertReport(filePath)
        return "Item Found!"
    else: 
        return "Error: couldn't find file in storage" , filePath

@app.get("/pinecone/{item_id}")
async def get_item(item_id: str | None = None):
    print(item_id)
    pc = Pinecone(api_key="pcsk_6qzJGA_5xUfNgGmkyDar5tSg2gANqTCzPVWQjutiDaHyDDvFW8KEefuAxHvY1UmXJXJD4J")
    index = pc.Index(host="aarontest-x2rea8e.svc.aped-4627-b74a.pinecone.io")
    results = index.search(
        namespace="example-namespace", 
        query={
            "inputs": {"text": item_id[1:len(item_id)-1:1]}, 
            "top_k": 5
        },
        fields=["category", "chunk_text"]
    )

    return str(results)


@app.get("/idsearch/{item_id}")
async def get_item(item_id: str | None = None):
    print(item_id)
    pc = Pinecone(api_key="pcsk_6qzJGA_5xUfNgGmkyDar5tSg2gANqTCzPVWQjutiDaHyDDvFW8KEefuAxHvY1UmXJXJD4J")
    index = pc.Index(host="aarontest-x2rea8e.svc.aped-4627-b74a.pinecone.io")
    results = index.search(
        namespace="example-namespace", 
        query={
            "id": item_id, 
            "top_k": 2
        },
        fields=["category", "chunk_text"]
    )

    return str(results)

#quarry by meta datas, paragraphs, or perhaps even outright file
#fastapi dev testAPI.py