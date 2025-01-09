from fastapi import FastAPI, File, UploadFile, HTTPException
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    allowed_types = ["application/pdf", "image/jpeg"]

    print(file.content_type)
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only PDF and JPEG files are allowed.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    return {"filename": file.filename, "content_type": file.content_type}

@app.get("/files/")
async def list_files():
    files = os.listdir(UPLOAD_DIR)
    return {"files": files}
