from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.ingrediente import Ingrediente
from ..schemas.ingrediente import IngredienteCreate, IngredienteUpdate

class IngredienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 10) -> list[Ingrediente]:
        query = select(Ingrediente).where(Ingrediente.deleted_at == None).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_by_id(self, id: int) -> Optional[Ingrediente]:
        query = select(Ingrediente).where(Ingrediente.id == id, Ingrediente.deleted_at == None)
        return self.session.exec(query).first()

    def create(self, datos: IngredienteCreate) -> Ingrediente:
        ingrediente = Ingrediente(**datos.model_dump())
        self.session.add(ingrediente)
        return ingrediente

    def update(self, ingrediente: Ingrediente, datos: IngredienteUpdate) -> Ingrediente:
        data = datos.model_dump(exclude_unset=True)
        ingrediente.sqlmodel_update(data)
        self.session.add(ingrediente)
        return ingrediente

    def soft_delete(self, ingrediente: Ingrediente) -> None:
        ingrediente.deleted_at = datetime.utcnow()
        self.session.add(ingrediente)