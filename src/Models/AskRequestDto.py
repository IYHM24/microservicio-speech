from pydantic import BaseModel

""" DTO para la solicitud de análisis, que contiene la entrada del usuario. """
class AskRequestDto(BaseModel):
    user_input: str 