import logging

from fastapi import APIRouter, Depends, HTTPException
from models.user import User
from schemas.user import UserCreate
from sqlalchemy.orm import Session

from db import get_db, get_redis

logger = logging.getLogger(__name__)


router = APIRouter()
redis_client = get_redis()

@router.get("/", tags=["users"])
async def users():
    return {"message": "Welcome to Users API"}

@router.get("/all")
def get_all_users(db: Session = Depends(get_db)):
    print("Fetching all users")
    users = db.query(User).all()
    return users

@router.get("/{username}", tags=["users"])
async def read_user(username: str, db: Session = Depends(get_db)):
    cached_item = redis_client.get(username)
    if cached_item:
        logger.info(f"Cache hit for user: {username}")
        return {"username": username, "cached": True, "data": cached_item.decode('utf-8')}
    logger.info(f"Cache miss for user: {username}, querying database")
    # If not in cache, query the database
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    redis_client.setex(username, 5, username)
    return user
    
@router.post("/create", tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(
        username=user.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User created")
    logger.debug(f"User created: {user.username}")
    
    return user

@router.post("/delete/{username}", tags=["users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = User(
        username=user.username,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User created")
    logger.debug(f"User created: {user.username}")
    
    return user
