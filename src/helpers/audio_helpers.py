import subprocess
import os
import soundfile as sf
import io

class audio_helpers:
    
    def evaluar_audio(wav_bytes: bytes) -> bool:
        try:
            ## Evaluar el audio utilizando soundfile para verificar que se pueda leer correctamente
            audio, sr = sf.read(io.BytesIO(wav_bytes))
            ## Metricas básicas del audio para verificar su calidad
            print("Audio shape:", audio.shape)
            print("Sample rate:", sr)
            print("Duration seconds:", len(audio) / sr)
            return True
        except Exception as e:
            print(f"Error al evaluar el audio: {e}")
            return False

    """ Función para convertir bytes de audio GSM a WAV utilizando ffmpeg """
    def convert_gsm_to_wav(gsm_bytes: bytes) -> bytes:
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
        return wav_bytes