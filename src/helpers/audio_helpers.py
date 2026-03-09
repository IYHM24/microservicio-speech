import subprocess
import os
from fastapi import UploadFile
import soundfile as sf
import io
from src.core.logger import get_logger

""" Clase para compatibilizar con UploadFile de FastApi """
class FastAPILikeUploadFile:
    def __init__(self, filename: str, data: bytes):
        self.filename = filename
        self._data = data
    async def read(self) -> bytes:
        return self._data
    async def close(self):
        self._data = None

""" 
    Clase con funciones helper para el procesamiento de audio, incluyendo evaluación de calidad,
    conversión de formatos y manejo de chunks de audio.
 """
class audio_helpers:
    
    logger = get_logger(__name__)
    
    """ Función para evaluar la calidad del audio antes de procesarlo, verificando que se pueda leer correctamente y obteniendo métricas básicas. """
    def evaluar_audio(self, wav_bytes: bytes) -> bool:
        try:
            ## Evaluar el audio utilizando soundfile para verificar que se pueda leer correctamente
            audio, sr = sf.read(io.BytesIO(wav_bytes))
            ## Metricas básicas del audio para verificar su calidad
            self.logger.debug(f"Audio shape: {audio.shape}")
            self.logger.debug(f"Sample rate: {sr}")
            self.logger.debug(f"Duration seconds: {len(audio) / sr}")
            return True
        except Exception as e:
            self.logger.error(f"Error al evaluar el audio: {e}")
            return False

    """ Función para convertir bytes de audio GSM a WAV utilizando ffmpeg """
    def convert_gsm_to_wav(self, gsm_bytes: bytes) -> bytes:
        # Determinar si el audio es estéreo o mono según la variable de entorno
        stereo = os.getenv("WHISPER_AUDIO_STEREO", "false").lower() == "true"
        # Crear un proceso de ffmpeg para convertir el audio GSM a WAV
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-i", "pipe:0",
                "-ar", "16000",
                "-ac", "2" if stereo else "1",
                "-f", "wav",
                "pipe:1"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        wav_bytes, _ = process.communicate(input=gsm_bytes)
        self.logger.info(f"Archivo GSM convertido a WAV, tamaño: {len(wav_bytes)} bytes")
        return wav_bytes

    """ Convertir los bytes recibidos de gRPC en UploadFile para ser procesados por las funciones de FastAPI """
    def chunks_to_audio(self, request_iterator: list) -> UploadFile:
        """ Función para convertir una lista de chunks de audio en un solo archivo de audio en bytes. """
        parts = []
        filename = None
        for i, chunk_msg in enumerate(request_iterator):
            if i == 0 and getattr(chunk_msg, "filename", None):
                filename = chunk_msg.filename
            parts.append(chunk_msg.chunk)  # chunk_msg.chunk es bytes
        audio_bytes = b"".join(parts)
        self.logger.info(f"Chunks combinados en un solo archivo de audio, tamaño total: {len(audio_bytes)} bytes")
        return FastAPILikeUploadFile(filename or "uploaded.gsm", audio_bytes)