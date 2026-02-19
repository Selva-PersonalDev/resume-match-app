import os
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from analyzer import analyze_resume
from file_parser import extract_text

APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="Resume Match Analyzer")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    try:
        resume_bytes = await resume_file.read()
        jd_bytes = await jd_file.read()

        resume_text = extract_text(resume_bytes, resume_file.filename)
        jd_text = extract_text(jd_bytes, jd_file.filename)

        result = analyze_resume(resume_text, jd_text)
        result["version"] = APP_VERSION

        return templates.TemplateResponse(
            "result.html",
            {"request": request, "result": result}
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
