import io,os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the "music" folder as a static directory
app.mount("/music", StaticFiles(directory="music"), name="music")

@app.post("/upload-music")
async def create_upload_file(file: UploadFile = File(...)):
    if not os.path.exists('music'):
        os.makedirs("music")
        file_location = os.path.join("music", file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())
    else:
        file_location = os.path.join("music", file.filename)
        with open(file_location, "wb") as buffer:
            buffer.write(await file.read())  
    return {"filename": file.filename,"status":200}

@app.get("/get-music")
def get_music():
    file_list = os.listdir("music")
    files = []
    if file_list:
        file_urls = [{"url":f"/music/{filename}","filename":{filename}} for filename in file_list]
        return {"file_urls": file_urls}
    else:
        return {"error": "No files found in the music folder."}