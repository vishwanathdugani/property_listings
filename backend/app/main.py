import logging
from datetime import datetime
from fastapi import FastAPI, Request
from app.api.endpoints import property as property_endpoint
from app.db.base import Base
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    logging.info(f"Timestamp: {start_time.strftime('%Y-%m-%d %H:%M:%S')} | Method: {request.method} | Path: {request.url.path} | Processing Time: {process_time}s")
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(property_endpoint.router)
