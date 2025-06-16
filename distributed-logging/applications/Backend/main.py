import logging
import signal
import sys
import time

from fastapi import FastAPI
from opentelemetry.sdk._logs import LoggingHandler

from db import init_db
from routes import user

init_db()

def shutdown_handler(signum, frame):
    logger.info("Received shutdown signal, cleaning up...")
    # Clean up resources here
    sys.exit(0)

signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

uvicorn_logger = logging.getLogger("uvicorn")
error_logger = logging.getLogger("uvicorn.error")
access_logger = logging.getLogger("uvicorn.access")

otel_handler = LoggingHandler(level=logging.NOTSET)
uvicorn_logger.addHandler(otel_handler)
error_logger.addHandler(otel_handler)
access_logger.addHandler(otel_handler)

# FastAPI app
app = FastAPI()
logger.debug("FastAPI app initialized", extra={"app": "Backend"})
logger.info("Starting FastAPI Backend application")

# Routes
app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
logger.debug("Routes included", extra={"route": "api/v1/users", "tags": ["users"]})

# Direct endpoints
@app.get("/")
def read_root():
    logger.debug("Root endpoint accessed")
    return {"message": "Hello from FastAPI"}

@app.get("/health")
def health_check():
    logger.debug("Health check endpoint accessed")
    return {"status": "ok"}
