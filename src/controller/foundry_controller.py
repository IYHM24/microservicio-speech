from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

from src.services.foundry_service import FoundryService
from src.helpers.audio_helpers import audio_helpers


class InvokeRequest(BaseModel):
    prompt: str
    options: dict = None


router = APIRouter(prefix="/foundry", tags=["Foundry"])
foundry_service = FoundryService()


@router.post("/invoke")
async def invoke(req: InvokeRequest):
    try:
        result = await foundry_service.call_model(req.prompt, req.options or {})
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # aceptar .gsm y otros formatos; convertir si es gsm
    file_bytes = await file.read()
    if file.filename.endswith(".gsm"):
        wav_bytes = audio_helpers.convert_gsm_to_wav(file_bytes)
    else:
        wav_bytes = file_bytes

    if not audio_helpers.evaluar_audio(wav_bytes):
        raise HTTPException(status_code=400, detail="Invalid audio file after conversion")

    try:
        result = await foundry_service.transcribe(wav_bytes)
        return {"filename": file.filename, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    is_healthy = await foundry_service.health_check()
    if is_healthy:
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=503, detail="Foundry service is unhealthy")