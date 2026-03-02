from pathlib import Path
from fastapi import FastAPI
from src.controller.openai_whisper_controller import router as whisper_router
from src.controller.health_controller import router as health_router
import os
import uvicorn

### Crear la instancia de la aplicación FastAPI
app = FastAPI(
    title="Whisper Service API",
    description="API para transcribir archivos de audio utilizando el modelo Whisper de OpenAI",
    version="1.0.0"
)

## Incluir los routers de las rutas definidas en los controladores
app.include_router(whisper_router)
app.include_router(health_router)

## Principal punto de entrada para ejecutar la aplicación
if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    uvicorn.run(app, host="0.0.0.0", port=port)

""" 
BASE_DIR = Path(__file__).parent
audio_path = (BASE_DIR / "assets" / "audios" / "test.gsm").resolve()

if not audio_path.exists():
    raise FileNotFoundError(f"Audio no encontrado: {audio_path}")

 """

#asyncio.run(transcribe_audio(audio_path))

