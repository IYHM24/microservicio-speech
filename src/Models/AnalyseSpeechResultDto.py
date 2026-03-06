from pydantic import BaseModel

class AnalyseSpeechResultDto(BaseModel):
    intent: str
    account_id: str
    product: str
    sentiment: str
    urgency: int