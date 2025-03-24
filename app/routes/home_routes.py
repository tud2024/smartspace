# Home router
from typing import Annotated
from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import service functions
from app.services.product_service import *
from app.services.category_service import getAllCategories

from app.models.product import Product

router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    categories = getAllCategories()  # Fetch only categories
    return templates.TemplateResponse("home/index.html", {"request": request, "categories": categories})

@router.get("/update/{id}", response_class=HTMLResponse)
async def getProfuctUpdateForm(request: Request, id: int):

    # note passing of parameters to the page
    return templates.TemplateResponse("product/partials/product_update_form.html", {"request": request, "product": getProduct(id), "categories": getAllCategories() })

@router.get("/bycat/{id}")
def delProduct(request: Request, id: int):
    products = getProductByCat(id)
    print(getProductByCat(id))
    return templates.TemplateResponse("product/partials/product_list.html", {"request": request, "products": products})


@router.post("/clicked", response_class=HTMLResponse)
async def clicked(request: Request):
    # note passing of parameters to the page
    return templates.TemplateResponse("home/partials/clicked_button.html", {"request": request })