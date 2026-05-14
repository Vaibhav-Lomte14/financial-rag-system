from fastapi import FastAPI

from app.database import engine, Base

from app.routes import auth_routes
from app.routes import document_routes
# from app.routes import rag_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():

    return {
        "message": "Financial RAG API Running"
    }

app.include_router(auth_routes.router)

app.include_router(document_routes.router)

# app.include_router(rag_routes.router)