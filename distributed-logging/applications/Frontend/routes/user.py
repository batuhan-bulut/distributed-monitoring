import os
import logging
import requests
from fastapi import APIRouter
import utils.api_utils as api

logger = logging.getLogger(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

router = APIRouter()

@router.get("/", tags=["users"])
async def users():
    return {"message": "Welcome to Users API"}

@router.get("/all")
async def get_all_users():
    logger.info("Fetching all users")
    response = await api.async_get_request(url=f"{BACKEND_URL}/api/v1/users/all")
    logger.debug(response)
    return response

@router.get("/{username}", tags=["users"])
async def read_user(username):
    logger.info(f"Fetching user with username: {username}")
    response = await api.async_get_request(url=f"{BACKEND_URL}/api/v1/users/{username}")
    logger.debug(response)
    return response

    
@router.post("/create", tags=["users"])
async def create_user(payload: dict):
    logger.info(f"Creating user with payload: {payload}")
    response = await api.async_post_request(f"{BACKEND_URL}/api/v1/users/create", json_data=payload)
    logger.debug(response)
    return response

# @router.post("/delete/{username}", tags=["users"])
# def create_user():

#     logger.info(f"User created")
#     return user
