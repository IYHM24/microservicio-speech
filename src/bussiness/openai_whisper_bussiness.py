from fastapi import UploadFile, File
from src.services.openai_service import OpenAiService
from src.services.whisper_service import WhisperService
from src.helpers.audio_helpers import audio_helpers
from src.Models.AnalyseSpeechTranscribeDto import AnalyseSpeechTranscribeDto
from test.mono_text_test import mono_text_test

class OpenAiWhisperBussiness:
    
    """ Constructor """
    def __init__(self):
        self.whisper_service = WhisperService()  # Instancia de la clase WhisperService
        self.openai_service = OpenAiService()  # Instancia de la clase OpenAiService
        self.audio_helpers = audio_helpers()  # Instancia de la clase audio_helpers

    """ Función para realizar una pregunta al modelo de OpenAI """
    def ask (self, user_input: str) -> dict:
        response = self.openai_service.ask(user_input)
        return {"response": response.content}

    """ Función para transcribir un archivo de audio (Formato .WAV) utilizando Whisper """
    async def transcribe_audio(self, file: UploadFile = File(...)):
        
        # Obtenemos los bytes del archivo GSM subido
        gsm_bytes = await file.read()
        
        ## Convertir el audio GSM a WAV utilizando la función del helper
        wav_bytes = self.audio_helpers.convert_gsm_to_wav(gsm_bytes)
        
        ## Evaluar el audio convertido para verificar su calidad
        if not self.audio_helpers.evaluar_audio(wav_bytes):
            return {"error": "Invalid audio file after conversion"}
        
        ## Transcribir el audio utilizando la función de la clase WhisperService
        #text = mono_text_test - solo para testear el análisis de texto sin necesidad de subir un archivo de audio
        text = self.whisper_service.transcribe_audio(wav_bytes)

        ## Devolver el resultado de la transcripción junto con el nombre del archivo
        return AnalyseSpeechTranscribeDto(
            filename=file.filename,
            text=text
        )
    
    """ Función para analizar el texto transcrito utilizando el modelo de OpenAI """
    def analyse_speech(self, transcribe_result: AnalyseSpeechTranscribeDto):
        # Aquí podrías implementar la lógica para analizar el texto transcrito utilizando el modelo de OpenAI
        # Por ejemplo, podrías enviar el texto a la función ask para obtener insights sobre intención, sentimiento, etc.
        analysis_result = self.openai_service.speech_analysis(transcribe_result)
        return analysis_result