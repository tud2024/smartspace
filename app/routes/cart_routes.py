from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import service functions
from app.services.product_service import *
from app.models.product import Product


router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

@router.get("/basket", response_class=HTMLResponse)
async def getCart(request: Request):
      return templates.TemplateResponse("cart/basket.html", {"request": request})
