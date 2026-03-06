from pydantic import BaseModel
from typing import Optional

class AnalyseSpeechResultDto(BaseModel):
    intent: str
    account_id: Optional[str] = None
    product: Optional[str] = None
    sentiment: Optional[str] = None