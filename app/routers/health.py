from fastapi import FastAPI, Header, Request, APIRouter
from typing import Optional
import base64
import json
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Configurer Jinja2 pour le rendu des templates
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/api")
def read_hello():
    return {"Hello": "Api"}


@router.get("/health")
def read_root():
    return {"message": "Api is running fine!"}


@router.get("/api/headers")
def read_hello(request: Request, x_userinfo: Optional[str] = Header(None, convert_underscores=True)):
    print(request["headers"])
    return {"Headers": json.loads(base64.b64decode(x_userinfo))}