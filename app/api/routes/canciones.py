# app/api/routes/canciones.py
from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.schemas.song import CancionOut
from app.schemas.album import AlbumOut

from app.factories import get_song_dao, get_album_dao
from app.dao.song_dao import SongDAO
from app.dao.album_dao import AlbumDAO

router = APIRouter(tags=["canciones"])

SONG_NOT_FOUND = "Canción no encontrada"

@router.get("/canciones", response_model=list[CancionOut])
def listar_canciones(
    genero: str | None = Query(None),
    popularidad: str | None = Query(None),
    song_dao: SongDAO = Depends(get_song_dao),
):
    return song_dao.list_songs(genero=genero, popularidad=popularidad)


# RF 4.3 - Obtener detalle de canción
@router.get("/canciones/{song_id}", response_model=CancionOut, summary="Obtener detalle de canción (RF-4.3)")
def get_song(song_id: int, song_dao: SongDAO = Depends(get_song_dao)):
    song = song_dao.get(song_id)
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=SONG_NOT_FOUND)
    return song

@router.delete("/canciones/{song_id}", status_code=204)
def borrar_cancion(song_id: int, song_dao: SongDAO = Depends(get_song_dao)):
    """Elimina una canción por su ID."""
    ok = song_dao.delete(song_id)
    if not ok:
        raise HTTPException(status_code=404, detail=SONG_NOT_FOUND)
    return None

@router.get("/artistas/{email_artista}/canciones", response_model=list[CancionOut])
def listar_canciones_por_artista(
    email_artista: str,
    song_dao: SongDAO = Depends(get_song_dao)
):
    """Lista las canciones de un artista dado su email."""
    return song_dao.get_by_artist(email_artista)

@router.get("/artistas/{email_artista}/albumes", response_model=list[AlbumOut])
def listar_albumes_por_artista(
    email_artista: str, album_dao: AlbumDAO = Depends(get_album_dao)
):
    """Lista los álbumes de un artista dado su email."""
    return album_dao.get_by_artist(email_artista)

# incrementa numVisualizaciones de una canción
@router.post("/canciones/{song_id}/play", response_model=CancionOut)
def registrar_reproduccion(
    song_id: int,
    song_dao: SongDAO = Depends(get_song_dao),
):
    song = song_dao.increment_views(song_id)
    if song is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SONG_NOT_FOUND,
        )
    return song

