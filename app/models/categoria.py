from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .producto import ProductoCategoria

class CategoriaBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)

class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["ProductoCategoria"] = Relationship(back_populates="categoria")

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaRead(CategoriaBase):
    id: int