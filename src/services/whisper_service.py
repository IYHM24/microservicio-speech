import io
import whisper
import soundfile as sf
import os
import numpy as np

class WhisperService:
    
    """ Constructor de la clase """
    def __init__(self):
        model_name = os.getenv("WHISPER_MODEL", "base")
        self.model = whisper.load_model(model_name)
        self.chunk_size = int(os.getenv("WHISPER_CHUNK_LENGTH", 30)) * 16000  # Convertir segundos a muestras

    """ Función para transcribir un canal de audio en fragmentos utilizando el modelo Whisper """
    def transcribir_canal(self, channel_audio, text_language):
        full_text = ""
        for i in range(0, len(channel_audio), self.chunk_size):
            #
            chunk = channel_audio[i:i + self.chunk_size]
            chunk = whisper.pad_or_trim(chunk)
            chunk = chunk.astype(np.float32)   
            #
            result = self.model.transcribe(
                chunk,
                language=text_language,
                temperature=0.0
            )
            #
            full_text += result["text"] + " "
        return full_text.strip()

    """ Función para transcribir un archivo de audio (Formato .WAV) """
    def transcribe_audio(self, audio_file):
        # Lenguaje del texto a transcribir.
        text_language = os.getenv("WHISPER_TEXT_LANGUAGE", "es")  # Puedes ajustar esto según el idioma de tus audios
        #  Convertir WAV bytes a numpy array correctamente
        audio, sample_rate = sf.read(io.BytesIO(audio_file))
        #Separar canales de audio si es estéreo
        
        """  """
        #if len(audio.shape) != 2:
            #raise Exception("El audio no es estéreo")
        #Canala de agente (izquierdo)
        #agent_text = self.transcribir_canal(audio[:, 0].astype(np.float32), text_language)
        #Canal de cliente (derecho)
        #client_text = self.transcribir_canal(audio[:, 1].astype(np.float32), text_language)
        """  """
        
        if audio.ndim > 1:
            mono = audio.mean(axis=1)
        else:
            mono = audio
        mono = mono.astype("float32")
        mono_text= self.transcribir_canal(mono, text_language)

        # Devolver un diccionario con las transcripciones de ambos canales
        return mono_text         
        