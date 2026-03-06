#Librerias
import os

#Modulos
from src.config.openai_config import OpenAiConfig

class OpenAiService( OpenAiConfig ):
    
    def __init__(self):
        super().__init__()
    
    """ Función para realizar una pregunta al modelo de OpenAI """
    def ask(self, user_input: str) -> dict:
        response = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=[
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
        )
        return response.choices[0].message
    

    
