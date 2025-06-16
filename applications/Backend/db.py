import os
import logging
import redis

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from models import Base

logger = logging.getLogger(__name__)

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_USER = os.getenv("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def create_psql_engine(
        host: str = POSTGRES_HOST, 
        port: int = POSTGRES_PORT, 
        user: str = POSTGRES_USER, 
        password: str = POSTGRES_PASSWORD, 
        dbname: str = POSTGRES_DB
        ):
    
    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    try:
        engine = create_engine(connection_url, echo=False, future=True)
        # Optionally test connection:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logging.info(f"PostgreSQL connnection successful")
    except OperationalError as e:
        raise Exception(f"Could not connect to PostgreSQL server: {e}") from e
    except Exception as e:
        raise Exception(f"An error occurred while connecting to PostgreSQL: {e}") from e

    return engine

def create_redis_engine(
        host: str = REDIS_HOST,
        port: int = REDIS_PORT,
        db: int = 0
        ):
    try:
        client = redis.Redis(host=host, port=port, db=db)
        # Optionally test connection:
        client.ping()  # This will raise an exception if the connection fails
        logging.info(f"Redis connection successful")
    except Exception as e:
        raise Exception(f"Could not connect to Redis server: {e}") from e

    return client

# Create engine
engine = create_psql_engine()
redis_client = create_redis_engine()
# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Initialize the redis client

def init_db():
    Base.metadata.create_all(bind=engine)

# Dependency to be used with FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_redis():
    return redis_client