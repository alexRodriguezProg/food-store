from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
if TYPE_CHECKING:
    from .producto import ProductoCategoria

class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    deleted_at: Optional[datetime] = Field(default=None)

    productos: List["ProductoCategoria"] = Relationship(back_populates="categoria")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaRead(CategoriaBase):
    id: int