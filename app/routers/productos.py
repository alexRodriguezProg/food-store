
from typing import Annotated
from fastapi import APIRouter, Query
from ..schemas.producto import ProductoCreate, ProductoRead, ProductoUpdate
from ..services.producto import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])
service = ProductoService()

@router.get("/", response_model=list[ProductoRead])
def listar_productos(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    return service.get_all(offset, limit)

@router.get("/{id}", response_model=ProductoRead)
def obtener_producto(id: int):
    return service.get_by_id(id)

@router.post("/", response_model=ProductoRead, status_code=201)
def crear_producto(datos: ProductoCreate):
    return service.create(datos)

@router.patch("/{id}", response_model=ProductoRead)
def actualizar_producto(id: int, datos: ProductoUpdate):
    return service.update(id, datos)

@router.delete("/{id}", status_code=204)
def eliminar_producto(id: int):
    service.delete(id)

