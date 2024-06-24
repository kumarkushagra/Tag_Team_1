from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import requests
# from Functions.Upload.upload import Upload
# from Functions.Download.main_download import download_studies
# from Functions.SCP.scp import scp_transfer
# from Functions.delete_studies.delete_studies import delete_all_studies
from Get_studies.get_studies import get_studies

app = FastAPI()

# Mount static files to serve HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_homepage():
    with open("static/HOMEpage.html") as f:
        return HTMLResponse(content=f.read(), media_type="text/html")

@app.get("/upload", response_class=HTMLResponse)
async def read_upload():
    with open("static/Upload.html") as f:
        return HTMLResponse(content=f.read(), media_type="text/html")

@app.post("/upload")
async def handle_upload(
    dir_path: str = Form(...),
    csv_path: str = Form(...),
    anonymization_flag: Optional[bool] = Form(False),
    batch_size: int = Form(...)
):
    Upload(dir_path, csv_path, anonymization_flag, batch_size)
    return {"message": "Upload data received"}

@app.get("/download", response_class=HTMLResponse)
async def read_download():
    with open("static/Download.html") as f:
        return HTMLResponse(content=f.read(), media_type="text/html")

@app.post("/download")
async def handle_download(
    download_dir_path: str = Form(...),
    study_ids: str = Form(...)
):
    study_ids_list = [id.strip() for id in study_ids.split(',')]
    download_studies(download_dir_path, study_ids_list)
    return {"message": "Download data received"}

@app.get("/scp-transfer", response_class=HTMLResponse)
async def read_scp_transfer():
    with open("static/SCP Transfer.html") as f:
        return HTMLResponse(content=f.read(), media_type="text/html")

@app.post("/scp-transfer")
async def handle_scp_transfer(
    source_host: str = Form(...),
    source_user: str = Form(...),
    source_file_path: str = Form(...),
    dest_host: str = Form(...),
    dest_user: str = Form(...),
    dest_file_path: str = Form(...),
    port: int = Form(...)
):
    try:
        scp_transfer(source_host, source_user, source_file_path, dest_host, dest_user, dest_file_path, port)
        return {"message": "SCP Transfer data received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/reprocess", response_class=HTMLResponse)
async def read_reprocess():
    with open("static/Reprocess.html") as f:
        return HTMLResponse(content=f.read(), media_type="text/html")

@app.post("/reprocess")
async def handle_reprocess(
    uhid: str = Form(...)
):
    delete_all_studies(uhid)
    return {"message": "Reprocess data received"}

@app.get("/get-studies-page", response_class=HTMLResponse)
async def read_get_studies_page():
    with open("static/GetStudies.html") as f:
        return HTMLResponse(content=f.read(), media_type="text/html")

@app.get("/get-studies", response_class=JSONResponse)
async def get_studies_endpoint():
    studies = get_studies()
    return {"studies": studies}

# To run the server, use the command: uvicorn main:app --reload
