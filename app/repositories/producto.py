from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.producto import Producto
from ..schemas.producto import ProductoCreate, ProductoUpdate

class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 10) -> list[Producto]:
        query = select(Producto).where(Producto.deleted_at == None).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_by_id(self, id: int) -> Optional[Producto]:
        query = select(Producto).where(Producto.id == id, Producto.deleted_at == None)
        return self.session.exec(query).first()

    def create(self, datos: ProductoCreate) -> Producto:
        producto = Producto(**datos.model_dump())
        self.session.add(producto)
        return producto

    def update(self, producto: Producto, datos: ProductoUpdate) -> Producto:
        data = datos.model_dump(exclude_unset=True)
        producto.sqlmodel_update(data)
        self.session.add(producto)
        return producto

    def soft_delete(self, producto: Producto) -> None:
        producto.deleted_at = datetime.utcnow()
        self.session.add(producto)