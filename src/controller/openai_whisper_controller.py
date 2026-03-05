from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from src.services.openai_service import OpenAiService
from src.services.whisper_service import WhisperService
from src.helpers.audio_helpers import audio_helpers
from src.Models.AskRequestDto import AskRequest

## Instancia del router para las rutas relacionadas con Whisper
router = APIRouter(prefix="/whisper", tags=["Whisper"])
whisper_service = WhisperService()  # Instancia de la clase WhisperService
openai_service = OpenAiService()  # Instancia de la clase OpenAiService

## Ruta para transcribir archivos GSM a texto utilizando Whisper
@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    ## Validar que el archivo sea del tipo GSM
    if not file.filename.endswith(".gsm"):
        return {"error": "Only .gsm files allowed"}
    gsm_bytes = await file.read()

    ## Convertir el audio GSM a WAV utilizando la función del helper
    wav_bytes = audio_helpers.convert_gsm_to_wav(gsm_bytes)
    
    ## Evaluar el audio convertido para verificar su calidad
    if not audio_helpers.evaluar_audio(wav_bytes):
        return {"error": "Invalid audio file after conversion"}

    ## Transcribir el audio utilizando la función de la clase WhisperService
    text = whisper_service.transcribe_audio(wav_bytes)

    return {
        "filename": file.filename,
        "text": text
    }

## Ruta para realizar una pregunta al modelo de OpenAI
## Recomendado solo para pruebas, no exponer en producción sin autenticación adecuada
@router.post("/ask")
async def ask(request: AskRequest):
    response = openai_service.ask(request.user_input)
    return {"response": response.content}
