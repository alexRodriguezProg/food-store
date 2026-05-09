from typing import Annotated
from fastapi import APIRouter, Query
from ..schemas.categoria import CategoriaCreate, CategoriaRead, CategoriaUpdate
from ..services.categoria import CategoriaService

router = APIRouter(prefix="/categorias", tags=["Categorías"])
service = CategoriaService()

@router.get("/", response_model=list[CategoriaRead])
def listar_categorias(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return service.get_all(offset, limit)

@router.get("/{id}", response_model=CategoriaRead)
def obtener_categoria(id: int):
    return service.get_by_id(id)

@router.post("/", response_model=CategoriaRead, status_code=201)
def crear_categoria(datos: CategoriaCreate):
    return service.create(datos)

@router.patch("/{id}", response_model=CategoriaRead)
def actualizar_categoria(id: int, datos: CategoriaUpdate):
    return service.update(id, datos)

@router.delete("/{id}", status_code=204)
def eliminar_categoria(id: int):
    service.delete(id)