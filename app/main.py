import os
from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from analyzer import analyze_resume
from file_parser import extract_text

APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="Resume Match Analyzer")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.post("/analyze")
async def analyze(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(None),
    jd_text: str = Form(None)
):
    try:
        resume_bytes = await resume_file.read()
        resume_text = extract_text(resume_bytes, resume_file.filename)

        if jd_file and jd_file.filename:
            jd_bytes = await jd_file.read()
            jd_content = extract_text(jd_bytes, jd_file.filename)
        elif jd_text and jd_text.strip():
            jd_content = jd_text.strip()
        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Provide JD file or JD text"}
            )

        result = analyze_resume(resume_text, jd_content)
        result["version"] = APP_VERSION

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
