# Home router

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from starlette.config import Config

router = APIRouter()

# Load environment variables from .env
config = Config(".env")

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the index.html page
@router.get("/", response_class=HTMLResponse)
async def index(request: Request):

    # get current date and time
    serverTime: datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    # note passing of parameters to the page
    return templates.TemplateResponse("./home/index.html", {"request": request, "serverTime": serverTime })






@router.post("/clicked", response_class=HTMLResponse)
async def clicked(request: Request):
    # note passing of parameters to the page
    return templates.TemplateResponse("./home/partials/clicked_button.html", {"request": request })

@router.get("/server_time", response_class=HTMLResponse)
async def index(request: Request):

    # get current date and time
    serverTime: datetime = datetime.now().strftime("%d/%m/%y %H:%M:%S")

    # send response
    return serverTime

