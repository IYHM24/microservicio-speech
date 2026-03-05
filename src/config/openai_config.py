import os
from openai import OpenAI

class OpenAiConfig:
    def __init__(self):
        # Definir las variables de entorno para la configuración de OpenAI
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.openai_base = os.getenv("OPENAI_BASE_URL")
        self.deployment_name = os.getenv("OPENAI_MODEL", "Kimi-K2.5")
        # Es importante validar que las variables de entorno necesarias estén definidas
        if not self.openai_base:
            raise RuntimeError("OPENAI_BASE_URL no definida")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY no definida. Usa setx o .env")
        # Inicializar el cliente de OpenAI con la configuración proporcionada
        self.client = OpenAI(
            base_url=self.openai_base,
            api_key=self.api_key
        )


