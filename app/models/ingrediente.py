from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

if TYPE_CHECKING:
    from .producto import ProductoIngrediente

class IngredienteBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    unidad_medida: str = Field(max_length=20)  # ej: "kg", "litros", "unidad"
    stock: float = Field(default=0.0, ge=0)

class Ingrediente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=100)
    unidad_medida: str = Field(max_length=20)
    stock: float = Field(default=0.0, ge=0)
    deleted_at: Optional[datetime] = Field(default=None)

    productos: List["ProductoIngrediente"] = Relationship(back_populates="ingrediente")

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteRead(IngredienteBase):
    id: int