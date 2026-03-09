from pydantic import BaseModel
from typing import Optional

""" DTO para el resultado del análisis de la transcripción de audio, incluyendo intención, cuenta, producto y sentimiento."""
class AnalyseSpeechResultDto(BaseModel):
    contexto: Optional[str] = None
    account_id: Optional[str] = None
    product: Optional[str] = None
    sentiment: Optional[str] = None
    Titular: Optional[str] = None