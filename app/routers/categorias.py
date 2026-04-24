from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..database import get_session
from ..models.categoria import Categoria, CategoriaCreate, CategoriaRead

router = APIRouter(prefix="/categorias", tags=["Categorías"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    nombre: Optional[str] = None,
):
    query = select(Categoria)
    if nombre:
        query = query.where(Categoria.nombre.contains(nombre))
    return session.exec(query.offset(offset).limit(limit)).all()

@router.get("/{categoria_id}", response_model=CategoriaRead)
def obtener_categoria(categoria_id: int, session: SessionDep):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaRead, status_code=201)
def crear_categoria(categoria: CategoriaCreate, session: SessionDep):
    db_categoria = Categoria.model_validate(categoria)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria

@router.patch("/{categoria_id}", response_model=CategoriaRead)
def actualizar_categoria(categoria_id: int, categoria: CategoriaCreate, session: SessionDep):
    db_categoria = session.get(Categoria, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    categoria_data = categoria.model_dump(exclude_unset=True)
    db_categoria.sqlmodel_update(categoria_data)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria

@router.delete("/{categoria_id}", status_code=204)
def eliminar_categoria(categoria_id: int, session: SessionDep):
    db_categoria = session.get(Categoria, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    session.delete(db_categoria)
    session.commit()