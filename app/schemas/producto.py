from typing import Optional
from sqlmodel import SQLModel

class ProductoCreate(SQLModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    disponible: bool = True

class ProductoRead(SQLModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    disponible: bool

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    disponible: Optional[bool] = None
