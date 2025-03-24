from typing import Annotated
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
import starlette.status as status
from fastapi.templating import Jinja2Templates
from app.models.user import RegisterUser

# import service functions
from app.services.auth_service import *

from app.models.user import User

router = APIRouter()

# set location for templates
templates = Jinja2Templates(directory="app/view_templates")


@router.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    # Get the cookie value
    user_first_name = request.cookies.get("user_first_name")

    # Pass it to the template
    return templates.TemplateResponse("base.html", {"user_first_name": user_first_name})





@router.get("/login", response_class=HTMLResponse)
async def getLogin(request: Request):
    

    # note passing of parameters to the page
    return templates.TemplateResponse("auth/login.html", {"request": request})

from fastapi.responses import RedirectResponse

@router.post("/login")
async def postLogin(request: Request, response: Response, userForm: Annotated[User, Form()]):
    # Step 1: Authenticate the user
    auth_user = userLogin(userForm)
    if auth_user and auth_user.session:
        # Step 2: Fetch user details, including roles
        user_details = supabase.table('users').select('*, roles(*)').eq('email', userForm.email).single().execute()

        if user_details.data:
            # Step 3: Extract user information
            first_name = user_details.data['first_name']
            role_data = user_details.data.get('roles')
            role_name = role_data['name'] if role_data else 'user'

            # Step 4: Set cookies for role and user info
            response.set_cookie(key="user_first_name", value=first_name, httponly=False)
            #response.set_cookie(key="user_role", value=role_name, httponly=False)  # Add this line here
            response.set_cookie(key="user_role", value=role_name, httponly=False)
            
            print(f"Cookie set: user_role={role_name}")  # Add debugging to verify

            print(f"User {first_name} logged in as {role_name}.")  # Debugging

            # Step 5: Redirect to the homepage or dashboard
            return RedirectResponse(url="/", status_code=302)
    
    # Handle login failure
    return templates.TemplateResponse(
        "auth/login.html", 
        {"request": request, "error": "Invalid credentials. Please try again."}
    )




#@router.post("/login")
#async def postLogin(request: Request, response: Response, userForm: Annotated[User, Form()]):
#    # Authenticate the user
#    auth_user = userLogin(userForm)
#    if auth_user and auth_user.session:
#        # Fetch user details from Supabase
#        user_details = supabase.table('users').select('*').eq('email', userForm.email).single().execute()
        
#        if user_details.data:  # Use .data to access the response content
#            first_name = user_details.data['first_name']
#            response.set_cookie(key="user_first_name", value=first_name, httponly=False)
#            print(f"Cookie Set: user_first_name={first_name}")  # Debugging
        
#        # Set access and refresh token cookies
#        response.set_cookie(key="access_token", value=auth_user.session.access_token, httponly=True)
#        response.set_cookie(key="refresh_token", value=auth_user.session.refresh_token, httponly=True)

#        return RedirectResponse(url="/", status_code=302)
    
#    # If authentication fails, return an error message
#    return templates.TemplateResponse("auth/login.html", {"request": request, "error": "Invalid credentials. Please try again."})
 



# Logout
@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("user_first_name")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return RedirectResponse(url="/", status_code=302)




@router.get("/register", response_class=HTMLResponse)
async def getRegister(request: Request):
    # note passing of parameters to the page
    return templates.TemplateResponse("auth/register.html", {"request": request})

@router.post("/register")
async def postRegister(request: Request, userForm: Annotated[RegisterUser, Form()]):
    try:
        # Step 1: Register the user in the auth.users table
        auth_user = supabase.auth.sign_up({
            "email": userForm.email,
            "password": userForm.password
        })

        # Check if registration was successful
        if not auth_user or not auth_user.user or not auth_user.user.id:
            return templates.TemplateResponse(
                "auth/register.html",
                {"request": request, "error": "Registration failed. Unable to create user in authentication system."}
            )

        # Retrieve the auth_id
        auth_id = auth_user.user.id
        print(f"Auth ID (UUID): {auth_id}")  # Debugging

        # Step 2: Insert into the users table
        user_data = {
            "auth_id": auth_id,  # Link the auth ID from auth.users
            "first_name": userForm.first_name,
            "last_name": userForm.last_name,
            "email": userForm.email,
            "phone": userForm.phone,
            "address": userForm.address,
        }

        response = supabase.table("users").insert(user_data).execute()

        # Verify if insertion was successful
        if not response.data:
            return templates.TemplateResponse(
                "auth/register.html",
                {"request": request, "error": "Failed to save user profile details. Please try again."}
            )

        # Step 3: Redirect to login page upon successful registration
        return RedirectResponse(
            url="/auth/login?message=Registration successful. Please log in.",
            status_code=status.HTTP_302_FOUND
        )

    except Exception as e:
        # Handle unexpected errors
        print(f"Error: {e}")  # Debugging
        return templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "error": f"An unexpected error occurred: {str(e)}"}
        )
   