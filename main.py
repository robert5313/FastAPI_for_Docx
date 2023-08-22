import os
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# importing required modules
# from PyPDF2 import PdfReader
import textract

DATA_DIR = "Data/"

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return "upload file to http://127.0.0.1:8000/file-upload"


@app.get("/file-upload", response_class=HTMLResponse)
def get_basic_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/file-upload", response_class=HTMLResponse)
async def post_basic_form(file: UploadFile = File(...)):
    print(f"Filename: {file.filename}")
    contents = await file.read()

    # save the file
    with open(f"{DATA_DIR}{file.filename}", "wb") as f:
        f.write(contents)

    file_path = f"./Data/{file.filename}"
    response = textract.process(file_path)

    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")

    return response
