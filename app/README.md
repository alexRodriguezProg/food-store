# Food Store API 🍽

Aplicación Fullstack desarrollada con FastAPI + React para la materia Programación IV.

## Tecnologías
- **Backend:** FastAPI, SQLModel, PostgreSQL, Python 3.12
- **Frontend:** React, TypeScript, TanStack Query, React Router, Tailwind CSS 4

## Estructura del proyecto

food-store/ → Backend (FastAPI)
food-store-frontend/ → Frontend (React)

## Cómo ejecutar

### Backend
```bash
cd food-store
source .venv/bin/activate
uvicorn app.main:app --port 8000 --reload
```

### Frontend
```bash
cd food-store-frontend
npm run dev
```

## Video de presentación
[Link al video aquí]

## Documentación de la API
Con el backend corriendo: http://localhost:8000/docs