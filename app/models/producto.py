from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from .categoria import Categoria, CategoriaRead
from .ingrediente import Ingrediente, IngredienteRead

# ── Tabla intermedia Producto ↔ Categoria (N:N) ──
class ProductoCategoria(SQLModel, table=True):
    producto_id: Optional[int] = Field(
        default=None, foreign_key="producto.id", primary_key=True
    )
    categoria_id: Optional[int] = Field(
        default=None, foreign_key="categoria.id", primary_key=True
    )
    producto: Optional["Producto"] = Relationship(back_populates="categorias")
    categoria: Optional[Categoria] = Relationship(back_populates="productos")

# ── Tabla intermedia Producto ↔ Ingrediente (N:N) ──
class ProductoIngrediente(SQLModel, table=True):
    producto_id: Optional[int] = Field(
        default=None, foreign_key="producto.id", primary_key=True
    )
    ingrediente_id: Optional[int] = Field(
        default=None, foreign_key="ingrediente.id", primary_key=True
    )
    cantidad: float = Field(default=1.0, gt=0)  # cuánto ingrediente lleva el producto
    producto: Optional["Producto"] = Relationship(back_populates="ingredientes")
    ingrediente: Optional[Ingrediente] = Relationship(back_populates="productos")

# ── Producto principal ──
class ProductoBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=255)
    precio: float = Field(gt=0)
    disponible: bool = Field(default=True)

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categorias: List[ProductoCategoria] = Relationship(back_populates="producto")
    ingredientes: List[ProductoIngrediente] = Relationship(back_populates="producto")

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int

# Schema enriquecido para mostrar relaciones en la UI
class ProductoReadDetalle(ProductoBase):
    id: int
    categorias: List[CategoriaRead] = []
    ingredientes: List[IngredienteRead] = []