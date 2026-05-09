from typing import Annotated
from fastapi import APIRouter, Query
from ..schemas.ingrediente import IngredienteCreate, IngredienteRead, IngredienteUpdate
from ..services.ingrediente import IngredienteService

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])
service = IngredienteService()

@router.get("/", response_model=list[IngredienteRead])
def listar_ingredientes(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return service.get_all(offset, limit)

@router.get("/{id}", response_model=IngredienteRead)
def obtener_ingrediente(id: int):
    return service.get_by_id(id)

@router.post("/", response_model=IngredienteRead, status_code=201)
def crear_ingrediente(datos: IngredienteCreate):
    return service.create(datos)

@router.patch("/{id}", response_model=IngredienteRead)
def actualizar_ingrediente(id: int, datos: IngredienteUpdate):
    return service.update(id, datos)

@router.delete("/{id}", status_code=204)
def eliminar_ingrediente(id: int):
    service.delete(id)