from fastapi import HTTPException
from ..uow.uow import UnitOfWork
from ..schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate

class IngredienteService:

    def get_all(self, offset: int, limit: int) -> list[IngredienteRead]:
        with UnitOfWork() as uow:
            ingredientes = uow.ingredientes.get_all(offset, limit)
            return [IngredienteRead.model_validate(i, from_attributes=True) for i in ingredientes]

    def get_by_id(self, id: int) -> IngredienteRead:
        with UnitOfWork() as uow:
            ingrediente = uow.ingredientes.get_by_id(id)
            if not ingrediente:
                raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
            return IngredienteRead.model_validate(ingrediente, from_attributes=True)

    def create(self, datos: IngredienteCreate) -> IngredienteRead:
        with UnitOfWork() as uow:
            ingrediente = uow.ingredientes.create(datos)
            uow.commit()
            uow.session.refresh(ingrediente)
            return IngredienteRead.model_validate(ingrediente, from_attributes=True)

    def update(self, id: int, datos: IngredienteUpdate) -> IngredienteRead:
        with UnitOfWork() as uow:
            ingrediente = uow.ingredientes.get_by_id(id)
            if not ingrediente:
                raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
            ingrediente = uow.ingredientes.update(ingrediente, datos)
            uow.commit()
            uow.session.refresh(ingrediente)
            return IngredienteRead.model_validate(ingrediente, from_attributes=True)

    def delete(self, id: int) -> None:
        with UnitOfWork() as uow:
            ingrediente = uow.ingredientes.get_by_id(id)
            if not ingrediente:
                raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
            uow.ingredientes.soft_delete(ingrediente)