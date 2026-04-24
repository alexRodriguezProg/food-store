from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from ..database import get_session
from ..models.producto import Producto, ProductoCreate, ProductoRead

router = APIRouter(prefix="/productos", tags=["Productos"])

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[ProductoRead])
def listar_productos(
    session: SessionDep,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    nombre: Optional[str] = None,
    disponible: Optional[bool] = None,
):
    query = select(Producto)
    if nombre:
        query = query.where(Producto.nombre.contains(nombre))
    if disponible is not None:
        query = query.where(Producto.disponible == disponible)
    return session.exec(query.offset(offset).limit(limit)).all()

@router.get("/{producto_id}", response_model=ProductoRead)
def obtener_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

@router.post("/", response_model=ProductoRead, status_code=201)
def crear_producto(producto: ProductoCreate, session: SessionDep):
    db_producto = Producto.model_validate(producto)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@router.patch("/{producto_id}", response_model=ProductoRead)
def actualizar_producto(producto_id: int, producto: ProductoCreate, session: SessionDep):
    db_producto = session.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    producto_data = producto.model_dump(exclude_unset=True)
    db_producto.sqlmodel_update(producto_data)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@router.delete("/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, session: SessionDep):
    db_producto = session.get(Producto, producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(db_producto)
    session.commit()