from fastapi import HTTPException
from ..uow.uow import UnitOfWork
from ..schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate

class CategoriaService:

    def get_all(self, offset: int, limit: int) -> list[CategoriaRead]:
        with UnitOfWork() as uow:
            categorias = uow.categorias.get_all(offset, limit)
            return [CategoriaRead.model_validate(c, from_attributes=True) for c in categorias]

    def get_by_id(self, id: int) -> CategoriaRead:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(id)
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            return CategoriaRead.model_validate(categoria, from_attributes=True)

    def create(self, datos: CategoriaCreate) -> CategoriaRead:
        with UnitOfWork() as uow:
            categoria = uow.categorias.create(datos)
            uow.commit()
            uow.session.refresh(categoria)
            return CategoriaRead.model_validate(categoria, from_attributes=True)

    def update(self, id: int, datos: CategoriaUpdate) -> CategoriaRead:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(id)
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            categoria = uow.categorias.update(categoria, datos)
            uow.commit()
            uow.session.refresh(categoria)
            return CategoriaRead.model_validate(categoria, from_attributes=True)

    def delete(self, id: int) -> None:
        with UnitOfWork() as uow:
            categoria = uow.categorias.get_by_id(id)
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            uow.categorias.soft_delete(categoria)