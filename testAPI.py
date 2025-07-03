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
        #return extraction(file.file)
        return {"filename": file.filename}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "Short was false :("}
        )
    return item


#fastapi dev testAPI.py