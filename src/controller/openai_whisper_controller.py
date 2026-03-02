from fastapi import APIRouter, UploadFile, File
from src.services.whisper_service import WhisperService
from src.helpers.audio_helpers import audio_helpers

## Instancia del router para las rutas relacionadas con Whisper
router = APIRouter(prefix="/whisper", tags=["Whisper"])
whisper_service = WhisperService()  # Instancia de la clase WhisperService

## Ruta para transcribir archivos GSM a texto utilizando Whisper
@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    ## Validar que el archivo sea del tipo GSM
    if not file.filename.endswith(".gsm"):
        return {"error": "Only .gsm files allowed"}
    gsm_bytes = await file.read()

    ## Convertir el audio GSM a WAV utilizando la función del helper
    wav_bytes = audio_helpers.convert_gsm_to_wav(gsm_bytes)

    ## Transcribir el audio utilizando la función de la clase WhisperService
    text = await WhisperService.transcribe_audio(wav_bytes)

    return {
        "filename": file.filename,
        "text": text
    }