from fastapi import UploadFile, File
from src.services.openai_service import OpenAiService
from src.services.whisper_service import WhisperService
from src.helpers.audio_helpers import audio_helpers
from src.Models.AnalyseSpeechTranscribeDto import AnalyseSpeechTranscribeDto

class OpenAiWhisperBussiness:
    
    """ Constructor """
    def __init__(self):
        self.whisper_service = WhisperService()  # Instancia de la clase WhisperService
        self.openai_service = OpenAiService()  # Instancia de la clase OpenAiService

    """ Función para realizar una pregunta al modelo de OpenAI """
    def ask (self, user_input: str) -> dict:
        response = self.openai_service.ask(user_input)
        return {"response": response.content}

    """ Función para transcribir un archivo de audio (Formato .WAV) utilizando Whisper """
    async def transcribe_audio(self, file: UploadFile = File(...)):
        
        # Obtenemos los bytes del archivo GSM subido
        gsm_bytes = await file.read()
        
        ## Convertir el audio GSM a WAV utilizando la función del helper
        wav_bytes = audio_helpers.convert_gsm_to_wav(gsm_bytes)
        
        ## Evaluar el audio convertido para verificar su calidad
        if not audio_helpers.evaluar_audio(wav_bytes):
            return {"error": "Invalid audio file after conversion"}
        
        ## Transcribir el audio utilizando la función de la clase WhisperService
        text = self.whisper_service.transcribe_audio(wav_bytes)
        
        ## Devolver el resultado de la transcripción junto con el nombre del archivo
        return AnalyseSpeechTranscribeDto(
            filename=file.filename,
            text=text
        )