from fastapi import HTTPException
from ..uow.uow import UnitOfWork
from ..schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate

class ProductoService:

    def get_all(self, offset: int, limit: int) -> list[ProductoRead]:
        with UnitOfWork() as uow:
            productos = uow.productos.get_all(offset, limit)
            return [ProductoRead.model_validate(p, from_attributes=True) for p in productos]

    def get_by_id(self, id: int) -> ProductoRead:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(id)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            return ProductoRead.model_validate(producto, from_attributes=True)

    def create(self, datos: ProductoCreate) -> ProductoRead:
        with UnitOfWork() as uow:
            producto = uow.productos.create(datos)
            uow.commit()
            uow.session.refresh(producto)
            return ProductoRead.model_validate(producto, from_attributes=True)

    def update(self, id: int, datos: ProductoUpdate) -> ProductoRead:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(id)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            producto = uow.productos.update(producto, datos)
            uow.commit()
            uow.session.refresh(producto)
            return ProductoRead.model_validate(producto, from_attributes=True)

    def delete(self, id: int) -> None:
        with UnitOfWork() as uow:
            producto = uow.productos.get_by_id(id)
            if not producto:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            uow.productos.soft_delete(producto)