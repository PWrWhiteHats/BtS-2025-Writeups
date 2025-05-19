import os
import shutil
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.concurrency import run_in_threadpool

from app.utils import *

MAX_TEXT_LENGTH = 3000
MAX_FILE_SIZE_KB = 100

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

templates = Jinja2Templates(directory="app/templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return PlainTextResponse("Too many requests. Slow down!", status_code=429)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit")
@limiter.limit("5/minute")
async def submit_report(request: Request, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
         
        file.file.seek(0, os.SEEK_END)
        file_size_kb = file.file.tell() / 1024
        file.file.seek(0)

        if file_size_kb > MAX_FILE_SIZE_KB:
             return {"result": "fail", "grade": "2.0", "description": f"Report is large. Limit is {MAX_FILE_SIZE_KB} KB."}

    pdf_text = await run_in_threadpool(extract_pdf_text, file_path)
    
    if (len(pdf_text) > MAX_TEXT_LENGTH):
        return {"result": "fail", "grade": "2.0", "description": f"Report is too long. Limit is {MAX_TEXT_LENGTH} characters."}
    
    try:
        ocr_text = await run_in_threadpool(ocr_pdf, file_path)
    except Exception as e:
        return {"result": "fail", "reason": "OCR fail", "description": f"{e}"}
    
    if (len(ocr_text) > MAX_TEXT_LENGTH):
        return {"result": "fail", "grade": "2.0", "description": f"Report is too long. Limit is {MAX_TEXT_LENGTH} characters."}

    if not check_report(ocr_text):
        return {"result": "fail", "reason": "OCR mismatch"}

    return_ai = await run_in_threadpool(grade_report, pdf_text)
    return_ai = return_ai.split("|")
    return_ai[1] = insert_line_breaks(return_ai[1].rstrip())

    with open("flag") as flag:
        if float(return_ai[0]) >= 5.0:
            return {"result": "success", "grade": return_ai[0], "flag": flag.read(), "description": return_ai[1].strip()}
        else:
            return {"result": "fail", "grade": return_ai[0], "description": return_ai[1].strip()}
