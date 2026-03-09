from pathlib import Path
from fastapi import FastAPI
from src.controller.openai_whisper_controller import router as whisper_router
from src.controller.health_controller import router as health_router
from src.controller.foundry_controller import router as foundry_router
from src.core.logger import get_logger
from src.gRPC.config.gRPC_config import initGrpc

import os
import uvicorn

# Logger
logger = get_logger("main")

### Crear la instancia de la aplicación FastAPI
app = FastAPI(
    title="Whisper Service API",
    description="API para transcribir archivos de audio utilizando el modelo Whisper de OpenAI",
    version="1.0.0"
)

## Incluir los routers de las rutas definidas en los controladores
app.include_router(whisper_router)
app.include_router(health_router)
app.include_router(foundry_router)

## Principal punto de entrada para ejecutar la aplicación
if __name__ == "__main__":

    port = int(os.getenv("PORT", 3000))

    # Limpiar la consola antes de iniciar la aplicación
    os.system("cls" if os.name == "nt" else "clear")

    # Iniciar el servidor gRPC - Ideal para ambiente de microservicios (Pruebas y Producción) - Fase Alpha no terminado
    #logger.info("Starting Speech Service gRPC server on port 50051")
    #initGrpc()

    # Iniciar el servidor API - Ideal conexion directa Frontend (Solo pruebas)
    logger.info(f"Starting Speech Service API on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)

