from pydantic import BaseModel

class AnalyseSpeechTranscribeDto(BaseModel):
    filename : str
    text : str
    language : str = "es"