from pydantic import BaseModel

""" DTO para la transcripción de audio, incluyendo el nombre del archivo, el texto transcrito y el idioma. """
class AnalyseSpeechTranscribeDto(BaseModel):
    filename : str
    text : str
    language : str = "es"