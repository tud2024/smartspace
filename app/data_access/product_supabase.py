# import the model class
from app.models.product import Product
from starlette.config import Config
from supabase import create_client, Client

import httpx, json

import json


# Load environment variables from .env
config = Config(".env")

db_url: str = config("SUPABASE_URL")
db_key: str = config("SUPABASE_KEY")

supabase: Client = create_client(db_url, db_key)


# get all products
def dataGetProducts():
    response = (supabase.table("product")
                .select("*, category(name)")
                .order("title", desc=False)
                .execute()
    )
    return response.data


def dataGetProductByCat(id: int) :
    response = (supabase.table("product")
                .select("*, category(name)")
                .eq("category_id", id)
                .order("title", desc=False)
                .execute()
    )
    return response.data
    

# get product by id
def dataGetProduct(id):
    # select * from product where id = id 
    response = (
        supabase.table("product")
        .select("*, category(name)")
        .eq("id", id)
        .execute()
    
    )
    return response.data[0]


# update product
def dataUpdateProduct(product: Product,accessToken, refreshToken) :
    supabase.auth.set_session(accessToken, refreshToken)
    # get the authenticted user
    auth_user = supabase.auth.get_user()
    # print the user id
    print('user id: ', auth_user.user.id)

    response = (
        supabase.table("product")
        .upsert(product.model_dump()) # convert product object to dict - required by Supabase
        .execute()
    )
    # result is 1st item in the list
    return response.data[0]

    
    

# add product, accepts product object
def dataAddProduct(product: Product, accessToken, refreshToken) :

    supabase.auth.set_session(accessToken, refreshToken)

    # get the authenticted user
    auth_user = supabase.auth.get_user()
    # print the user id for debugging purposes.
    # print('user id: ', auth_user.user.id)
    user_id= auth_user.user.id
    product_data = product.dict()  # Convert the Pydantic model to a dictionary
    product_data['user_id'] = user_id

    response = (
        supabase
        .table("product")
        .insert(product_data) # convert product object to dict - required by Supabase
        .execute()
    )

    if (response.data) :
        return dataGetProduct(response.data[0]['id'])

    return False

# get all categories
def dataGetCategories():
    response = (supabase.table("category")
                .select("*")
                .order("name", desc=False)
                .execute()
    )

    return response.data


# delete product by id
def dataDeleteProduct(id, accessToken, refreshToken):

    supabase.auth.set_session(accessToken, refreshToken)
    # select * from product where id = id 
    response = (
        supabase.table("product")
        .delete()
        .eq('id', id)
        .execute()
    )
    return response.data


# Supabase Auth for Python https://supabase.com/docs/reference/python/auth-api

# register new user
def dataUserRegister(user):
    response = supabase.auth.sign_up(user.model_dump())
    return response

# Login
def dataUserLogin(user):
    response = supabase.auth.sign_in_with_password(user.model_dump())
    return response

#Logout
def dataUserLogout():
    response = supabase.auth.sign_out()
    return "success"

# Get Session
def dataGetUserSession():
    response = supabase.auth.get_session()
    return response

# Supabase Auth for Python https://supabase.com/docs/reference/python/auth-api

# register new user
def dataUserRegister(user):
    response = supabase.auth.sign_up(user.model_dump())
    return response

def Data_Search(query: str, search_type: str = "word", category_name: str = None):
    """Fetches search results from Supabase based on search type and category name."""
    
    query_filter = supabase.table("product").select("*")

    # Apply category filter if category_name is provided
    if category_name:
        query_filter = query_filter.eq("category.name", category_name)  # Assuming category.name exists

    # Apply search type filters
    if search_type == "alphabet":
        query_filter = query_filter.ilike("title", f"{query}%")  # Titles starting with `query`
    
    elif search_type == "multiple":
        query_filter = query_filter.or_(
            f"title.ilike.%{query[0]}%,title.ilike.%{query[1]}%"  # Multiple letter match
        )
    
    elif search_type == "word":
        query_filter = query_filter.ilike("title", f"%{query}%")  # Partial word match
    
    else:
        return {"error": "Invalid search type"}

    # Execute the query and return the results
    response = query_filter.execute()
    return response.data  # Return raw database results
