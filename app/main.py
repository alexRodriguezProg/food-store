from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from .routers import categorias, ingredientes, productos

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Food Store API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categorias.router)
app.include_router(ingredientes.router)
app.include_router(productos.router)

@app.get("/")
def root():
    return {"message": "Food Store API funcionando ✅"}