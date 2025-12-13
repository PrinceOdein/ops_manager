from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import user  # noqa
from app.core.database import Base, engine
from app.api import users

app = FastAPI(title="Ops Manager", version="1.0.0")
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="app/templates")

print("Ops Manager is running...")

app.include_router(users.router)

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    return {"message": "Welcome to Ops Manager!"}

@app.get("/health")
def read_health():
    return {"status": "ok", "message": "Ops Manager is running smoothly."}