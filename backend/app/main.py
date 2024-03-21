from fastapi import FastAPI
from app.api.endpoints import property as property_endpoint
from app.db.base import Base
from app.db.database import engine
from fastapi.middleware.cors import CORSMiddleware

# Generate the database schema
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Include your routers here
app.include_router(property_endpoint.router)
