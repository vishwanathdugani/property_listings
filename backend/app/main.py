import logging
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from starlette import status
from fastapi.responses import JSONResponse

from app.core.auth import verify_token, oauth2_scheme
from app.api.endpoints import property as property_endpoint
from app.db.base import Base
from app.db.database import engine
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def request_processor(request: Request, call_next):
    """
        Middleware to process each incoming request.
        Validates the access token for all routes except the login route.
        Measures and logs the request processing time.

        Args:
            request (Request): The incoming request.
            call_next: The next middleware or route handler.

        Returns:
            Response: The response object to be sent back to the client.
    """
    start_time = datetime.now()

    if request.url.path not in ["/token", "/docs","/openapi.json"]:
        token = await oauth2_scheme(request)
        if not token:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Not authenticated"})
        try:
            verify_token(token, credentials_exception=HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ))
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

    response = await call_next(request)

    process_time = (datetime.now() - start_time).total_seconds()
    logging.info(
        f"Timestamp: {start_time.strftime('%Y-%m-%d %H:%M:%S')} | Method: {request.method}"
        f" | Path: {request.url.path} | Processing Time: {process_time}s")

    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
        Middleware for logging details of each request.
        Note: This seems to replicate part of the functionality in request_processor.
        Consider combining them if logging is the only purpose of this middleware.

        Args:
            request (Request): The incoming request.
            call_next: The next middleware or route handler.

        Returns:
            Response: The response object to be sent back to the client.
    """
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    logging.info(f"Timestamp: {start_time.strftime('%Y-%m-%d %H:%M:%S')} | "
                 f"Method: {request.method} | Path: {request.url.path} | Processing Time: {process_time}s")
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(property_endpoint.router)
