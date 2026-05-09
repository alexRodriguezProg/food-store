from typing import Optional
from sqlmodel import SQLModel

class IngredienteCreate(SQLModel):
    nombre: str
    unidad_medida: str
    stock: float = 0.0

class IngredienteRead(SQLModel):
    id: int
    nombre: str
    unidad_medida: str
    stock: float

class IngredienteUpdate(SQLModel):
    nombre: Optional[str] = None
    unidad_medida: Optional[str] = None
    stock: Optional[float] = None