from fastapi import APIRouter, UploadFile, File
from src.Models.AskRequestDto import AskRequestDto
from src.bussiness.openai_whisper_bussiness import OpenAiWhisperBussiness
from src.core.logger import get_logger

## Logger
logger = get_logger(__name__)

## Instancia del router para las rutas relacionadas con Whisper
router = APIRouter(prefix="/whisper", tags=["Whisper"])

## clase negocio
bussiness = OpenAiWhisperBussiness()  # Instancia de la clase OpenAiWhisperBussiness

""" Ruta para transcribir un archivo de audio utilizando Whisper """
@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    logger.info(f"Nueva solicitud de transcripción para el archivo: {file.filename}")
    ## Validar que el archivo sea del tipo GSM
    if not file.filename.endswith(".gsm"):
        logger.warning(f"Archivo no permitido: {file.filename}")
        return {"error": "Only .gsm files allowed"} 
    ## Transcribir el audio 
    logger.info(f"Transcribiendo el archivo de audio: {file.filename}")
    result = await bussiness.transcribe_audio(file)
    return result

""" Ruta para analizar un archivo de audio"""
@router.post("/analyse")
async def analyse(file: UploadFile = File(...)):
    logger.info(f"Nueva solicitud de análisis para el archivo: {file.filename}")
    ## Validar que el archivo sea del tipo GSM
    if not file.filename.endswith(".gsm"):
        logger.warning(f"Archivo no permitido: {file.filename}")
        return {"error": "Only .gsm files allowed"} 
    ## Transcribir el audio 
    logger.info(f"Transcribiendo el archivo de audio: {file.filename}")
    result = await bussiness.transcribe_audio(file)
    ## Analizar el resultado de la transcripción (Speech analysis)
    logger.info(f"Analizando la transcripción del archivo: {file.filename}")
    result = bussiness.analyse_speech(result)
    ## Retornar el resultado del análisis
    logger.info(f"Análisis completado para el archivo: {file.filename}")
    return result

""" Ruta para realizar una pregunta al LLM"""
@router.post("/ask")
async def ask(request: AskRequestDto):
    logger.info(f"se recibio una pregunta de {len(request.user_input)} caracteres")
    response = bussiness.ask(request.user_input)
    logger.info(f"se obtuvo una respuesta de {len(response['response'])} caracteres")
    return {"response": response["response"]}
