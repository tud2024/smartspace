from typing import Annotated
from fastapi import APIRouter, Form, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import service functions
from app.services.product_service import *
from app.services.product_service import get_Search_Data
from app.services.category_service import getAllCategories
from typing import Optional
from app.models.product import Product

router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the todos page
@router.get("/", response_class=HTMLResponse)
async def getProducts(request: Request):

    products = getAllProducts()
    categories = getAllCategories()

    # note passing of parameters to the page
    return templates.TemplateResponse("product/products.html", {"request": request, "products": products, "categories": categories })

# Return a only one product 

@router.get("/product/{id}")
def getProductDetails(request: Request, id: int):
    product = getProduct(id)
    return templates.TemplateResponse("product/partials/product_details.html", {"request": request, "product": product})
    

@router.get("/update/{id}", response_class=HTMLResponse)
async def getProfuctUpdateForm(request: Request, id: int):

    # note passing of parameters to the page
    return templates.TemplateResponse("product/partials/product_update_form.html", {"request": request, "product": getProduct(id), "categories": getAllCategories() })

# https://fastapi.tiangolo.com/tutorial/request-form-models/#pydantic-models-for-forms
@router.put("/")
def putProduct(request: Request, productData: Annotated[Product, Form()]) :
    accessToken = request.cookies.get('access_token')
    refreshToken = request.cookies.get('refresh_token')
    # get item value from the form POST data
    update_product = updateProduct(productData, accessToken, refreshToken)
    return templates.TemplateResponse("product/partials/product_tr.html", {"request": request, "product": update_product})

@router.post("/")
def postProduct(request: Request, productData: Annotated[Product, Form()]) :
    accessToken = request.cookies.get('access_token')
    refreshToken = request.cookies.get('refresh_token')

    # get item value from the form POST data
    new_product = newProduct(productData, accessToken, refreshToken)

    return templates.TemplateResponse("product/partials/product_tr.html", {"request": request, "product": new_product})

# https://fastapi.tiangolo.com/tutorial/request-form-models/#pydantic-models-for-forms

@router.delete("/{id}")
def delProduct(request: Request, id: int):
    accessToken = request.cookies.get('access_token')
    refreshToken = request.cookies.get('refresh_token')
    deleteProduct(id, accessToken, refreshToken)
    return templates.TemplateResponse("product/partials/product_list.html", {"request": request, "products": getAllProducts()})


@router.get("/bycat/{id}")
def delProduct(request: Request, id: int):
    products = getProductByCat(id)
    return templates.TemplateResponse("product/partials/product_flex.html", {"request": request, "products": products})

#@router.get("/search/")
#async def live_search(request: Request, query: str):
#    # Call get_Search_Data synchronously, no await
#    results = get_Search_Data(query)

#    # Return the rendered template with the search results
#    return templates.TemplateResponse("product/partials/search_results.html", {"request": request, "results": results})

@router.get("/search/")
async def live_search(request: Request, query: str, search_type: str = "word", category_name: str = None):
    # Get raw results from Supabase
    raw_results = Data_Search(query, search_type, category_name)

    # Check if raw_results is not empty
    if not raw_results:
        return "No results found or invalid data." 

    # Convert the raw results into Product objects
    results = [Product(**item) for item in raw_results if isinstance(item, dict)]

    return templates.TemplateResponse(
        "product/partials/search_results.html", 
        {"request": request, "results": results}
    )
