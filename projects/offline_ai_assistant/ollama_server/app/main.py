from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from .train import process_file
from fastapi import Form
from .query import search_and_respond
from pathlib import Path

app = FastAPI()
# templates = Jinja2Templates(directory="templates")
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

UPLOAD_DIR = "/tmp/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/train")
async def train(request: Request, file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        result = process_file(file_path)
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "message": f"Training complete: {result}"
        })
    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": str(e)
        })
@app.post("/ask")
async def ask_question(request: Request, question: str = Form(...), dataset: str = Form(None)):
    try:
        answer = search_and_respond(question, dataset_name=dataset)
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "answer": answer,
            "question": question,
            "dataset": dataset
        })
    except Exception as e:
        return templates.TemplateResponse("upload.html", {
            "request": request,
            "error": str(e)
        })
