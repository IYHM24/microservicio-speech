from pydantic import BaseModel

# Modelo de datos para la solicitud de la ruta /ask
class AskRequestDto(BaseModel):
    user_input: str