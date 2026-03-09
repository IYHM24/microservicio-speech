from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])

""" Ruta para el health check del servicio, que simplemente devuelve un estado "ok". """
@router.get("/check")
async def health_check():
    return {"status": "ok"}