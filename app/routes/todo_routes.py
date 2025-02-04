from typing import Annotated
from fastapi import APIRouter, Form
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# import service functions
from app.services.todo_service import getAllTodos, getTodo, addTodo, updateTodo, deleteTodo

from app.models.todo import ToDo

router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")

# handle http get requests for the site root /
# return the todos page
@router.get("/", response_class=HTMLResponse)
async def getTodos(request: Request, filter : str | None = "all"):

    # note passing of parameters to the page
    return templates.TemplateResponse("todo/todos.html", {"request": request, "todoList": getAllTodos(), "filter": "all" })

@router.get("/update/{id}", response_class=HTMLResponse)
async def getTodo(request: Request, id: int):

    # note passing of parameters to the page
    return templates.TemplateResponse("todo/partials/todo_update_form.html", {"request": request, "todo": getTodo(id) })

@router.get("/filter/{filter}", response_class=HTMLResponse)
async def getTodosFilter(request: Request, filter: str):

    # note passing of parameters to the page
    return templates.TemplateResponse("todo/partials/todo_list.html", {"request": request, "todoList": getAllTodos(), "filter": filter   })



@router.post("/")
def postTodo(request: Request, item: str = Form(...)):

    # get item value from the form POST data
    new_todo = addTodo(item)
    return templates.TemplateResponse("todo/partials/todo_li.html", {"request": request, "todo": new_todo})

@router.put("/")
def putTodo(request: Request, id: Annotated[int, Form()], details: Annotated[str, Form()], completed: Annotated[str, Form()] = ""):
    # get item value from the form POST data

    up_todo = updateTodo(id, details, completed)
    return templates.TemplateResponse("todo/partials/todo_li.html", {"request": request, "todo": up_todo})

@router.delete("/{id}")
def delToto(request: Request, id: int):
    deleteTodo(id)
    return templates.TemplateResponse("todo/partials/todo_list.html", {"request": request, "todoList": getAllTodos(), "filter": "all" })
