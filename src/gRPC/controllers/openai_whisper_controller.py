
from src.gRPC.stubs import speech_service_pb2, speech_service_pb2_grpc
from src.controller.openai_whisper_controller import transcribe, analyse, ask
from src.core.logger import get_logger
from src.helpers.audio_helpers import audio_helpers

logger = get_logger("openai_whisper_controller")
audio_helpers = audio_helpers()  

class SpeechService(speech_service_pb2_grpc.SpeechServiceServicer):
    
    """ 
    Transcribir el audio recibido en formato de chunks a texto utilizando
    la función transcribe del controlador de OpenAI Whisper 
    """
    def Transcribe(self, request, context):
        logger.info("Transcribe request received - gRPC")
        ##Convertir los chunks de audio recibidos en un archivo de audio compatible con FastAPI
        audio = audio_helpers.chunks_to_audio(request)
        result = transcribe(audio)
        return speech_service_pb2.TranscribeResponse(text=result)

    """ 
    Analizar el audio recibido en formato de chunks utilizando la función analyse del controlador de OpenAI Whisper,
    que incluye análisis de sentimiento, detección de emociones y otras métricas relacionadas con el habla. 
    """
    def Analyse(self, request, context):
        logger.info("Analyse request received - gRPC")
        audio = audio_helpers.chunks_to_audio(request)
        result = analyse(audio)
        return speech_service_pb2.AnalyseResponse(result=result)

    """ 
    Recibir una pregunta en formato de texto, procesarla utilizando 
    la función ask del controlador de OpenAI Whisper, que se encarga 
    de enviar la pregunta a un modelo de lenguaje (LLM) y obtener una
    respuesta basada en el contexto del audio transcrito. 
    """
    def Ask(self, request, context):
        logger.info(f"Ask request received - gRPC with input length: {len(request.user_input)}")
        response = ask(request.user_input)
        return speech_service_pb2.AskResponse(response=response)
