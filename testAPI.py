from fastapi import FastAPI, File, UploadFile
from converter import extraction
import os
import shutil

app = FastAPI()


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


#fastapi dev testAPI.py