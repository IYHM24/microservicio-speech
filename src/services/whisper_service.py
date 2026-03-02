import whisper
import os

class WhisperService:
    
    """ Constructor de la clase """
    def __init__(self):
        model_name = os.getenv("WHISPER_MODEL", "base")
        self.model = whisper.load_model(model_name)

    """ Función para transcribir un archivo de audio (Formato .WAV) """
    async def transcribe_audio(self, audio_file):
        text_language = os.getenv("WHISPER_TEXT_LANGUAGE", "es")  # Puedes ajustar esto según el idioma de tus audios
        result = await self.model.transcribe(
            audio_file,
            language=text_language,
            temperature=0.0
        )
        return result.get("text", "")