# app/api/routes/__init__.py
from fastapi import APIRouter
from .canciones import router as canciones_router
from .canciones_upload import router as canciones_upload_router
from .generos import router as generos_router
from .album import router as album_router
from .album_upload import router as album_upload_router
from .compras import router as compras_router
from .playlists import router as playlists_router
from .comentarios import router as comentarios_router

api_router = APIRouter(prefix="/api")
api_router.include_router(canciones_router)
api_router.include_router(canciones_upload_router)
api_router.include_router(generos_router)
api_router.include_router(compras_router)
api_router.include_router(album_router)
api_router.include_router(album_upload_router)
api_router.include_router(playlists_router)
api_router.include_router(comentarios_router)




