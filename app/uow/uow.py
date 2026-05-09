from sqlmodel import Session
from ..database import engine
from ..repositories.categoria import CategoriaRepository
from ..repositories.ingrediente import IngredienteRepository
from ..repositories.producto import ProductoRepository

class UnitOfWork:
    def __init__(self):
        self.session = Session(engine)
        self.categorias = CategoriaRepository(self.session)
        self.ingredientes = IngredienteRepository(self.session)
        self.productos = ProductoRepository(self.session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()