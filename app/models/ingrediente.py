from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .producto import ProductoIngrediente

class IngredienteBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    unidad_medida: str = Field(max_length=20)  # ej: "kg", "litros", "unidad"
    stock: float = Field(default=0.0, ge=0)

class Ingrediente(IngredienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["ProductoIngrediente"] = Relationship(back_populates="ingrediente")

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteRead(IngredienteBase):
    id: int