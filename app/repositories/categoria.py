from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.categoria import Categoria
from ..schemas.categoria import CategoriaCreate, CategoriaUpdate

class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 10) -> list[Categoria]:
        query = select(Categoria).where(Categoria.deleted_at == None).offset(offset).limit(limit)
        return self.session.exec(query).all()

    def get_by_id(self, id: int) -> Optional[Categoria]:
        query = select(Categoria).where(Categoria.id == id, Categoria.deleted_at == None)
        return self.session.exec(query).first()

    def create(self, datos: CategoriaCreate) -> Categoria:
        categoria = Categoria(**datos.model_dump())
        self.session.add(categoria)
        return categoria

    def update(self, categoria: Categoria, datos: CategoriaUpdate) -> Categoria:
        data = datos.model_dump(exclude_unset=True)
        categoria.sqlmodel_update(data)
        self.session.add(categoria)
        return categoria

    def soft_delete(self, categoria: Categoria) -> None:
        categoria.deleted_at = datetime.utcnow()
        self.session.add(categoria)