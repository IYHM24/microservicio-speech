from pydantic import BaseModel

# Modelo de datos para la solicitud de la ruta /ask
class AskRequest(BaseModel):
    user_input: str