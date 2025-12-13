from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Ops Manager", version="1.0.0")
templates = Jinja2Templates(directory="app/templates")

print("Ops Manager is running...")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    return {"message": "Welcome to Ops Manager!"}

@app.get("/health")
def read_health():
    return {"status": "ok", "message": "Ops Manager is running smoothly."}