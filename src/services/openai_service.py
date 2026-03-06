#Librerias
import json
import os

#Modulos
from src.config.openai_config import OpenAiConfig
from src.Models.AnalyseSpeechResultDto import AnalyseSpeechResultDto
from src.Models.AnalyseSpeechTranscribeDto import AnalyseSpeechTranscribeDto
from src.helpers.helpers import Helpers

class OpenAiService( OpenAiConfig ):
    
    def __init__(self):
        super().__init__()
    
    def build_messages(self, system_prompt: str, result: AnalyseSpeechTranscribeDto) -> list:
        user_content =  "Transcripcion: "+result.text + " language: "+ result.language
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

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
    
    def speech_analysis(self, AnalyseSpeechTranscribeDto ) -> AnalyseSpeechResultDto:
        ## Cargar el contrato
        schema = Helpers.load_schema("speech_analysis")
        system_prompt = Helpers.load_prompt("speech_analysis")
        ## Construir los mensajes para el análisis
        messages = self.build_messages(system_prompt, AnalyseSpeechTranscribeDto)
        ## Analysis
        analysis = self.client.chat.completions.create(
            model = self.deployment_name,
            messages = messages,
            response_format={
                "type": "json_schema",
                "json_schema": schema
            }
        )
        # Extraer el contenido de la respuesta y convertirlo a AnalyseSpeechResultDto
        analysis_content = analysis.choices[0].message.content
        analysis_json = json.loads(analysis_content)
        analysis_result = AnalyseSpeechResultDto(**analysis_json)
        # Retornar el resultado del analisis
        return analysis_result

