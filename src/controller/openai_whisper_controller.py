from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from src.services.openai_service import OpenAiService
from src.services.whisper_service import WhisperService
from src.helpers.audio_helpers import audio_helpers
from src.Models.AskRequestDto import AskRequestDto
from src.bussiness.openai_whisper_bussiness import OpenAiWhisperBussiness

## Instancia del router para las rutas relacionadas con Whisper
router = APIRouter(prefix="/whisper", tags=["Whisper"])

whisper_service = WhisperService()  # Instancia de la clase WhisperService
openai_service = OpenAiService()  # Instancia de la clase OpenAiService
bussiness = OpenAiWhisperBussiness()  # Instancia de la clase OpenAiWhisperBussiness

## Ruta para transcribir archivos GSM a texto utilizando Whisper
@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    
    ## Validar que el archivo sea del tipo GSM
    if not file.filename.endswith(".gsm"):
        return {"error": "Only .gsm files allowed"}
    
    ## Transcribir el audio 
    result = await bussiness.transcribe_audio(file)

    ## Analizar el resultado de la transcripción (Speech analysis)
    
    return result

## Ruta para realizar una pregunta al modelo de OpenAI
## Recomendado solo para pruebas, no exponer en producción sin autenticación adecuada
@router.post("/ask")
async def ask(request: AskRequestDto):
    response = bussiness.ask(request.user_input)
    return {"response": response["response"]}
