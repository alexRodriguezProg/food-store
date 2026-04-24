from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..database import get_session
from ..models.ingrediente import Ingrediente, IngredienteCreate, IngredienteRead

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[IngredienteRead])
def listar_ingredientes(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    nombre: Optional[str] = None,
):
    query = select(Ingrediente)
    if nombre:
        query = query.where(Ingrediente.nombre.contains(nombre))
    return session.exec(query.offset(offset).limit(limit)).all()

@router.get("/{ingrediente_id}", response_model=IngredienteRead)
def obtener_ingrediente(ingrediente_id: int, session: SessionDep):
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

@router.post("/", response_model=IngredienteRead, status_code=201)
def crear_ingrediente(ingrediente: IngredienteCreate, session: SessionDep):
    db_ing = Ingrediente.model_validate(ingrediente)
    session.add(db_ing)
    session.commit()
    session.refresh(db_ing)
    return db_ing

@router.patch("/{ingrediente_id}", response_model=IngredienteRead)
def actualizar_ingrediente(ingrediente_id: int, ingrediente: IngredienteCreate, session: SessionDep):
    db_ing = session.get(Ingrediente, ingrediente_id)
    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    ing_data = ingrediente.model_dump(exclude_unset=True)
    db_ing.sqlmodel_update(ing_data)
    session.add(db_ing)
    session.commit()
    session.refresh(db_ing)
    return db_ing

@router.delete("/{ingrediente_id}", status_code=204)
def eliminar_ingrediente(ingrediente_id: int, session: SessionDep):
    db_ing = session.get(Ingrediente, ingrediente_id)
    if not db_ing:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    session.delete(db_ing)
    session.commit()