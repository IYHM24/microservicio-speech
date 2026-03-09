
from src.gRPC.stubs import speech_Service_pb2, speech_Service_pb2_grpc
from src.controller.openai_whisper_controller import transcribe, analyse, ask
from src.core.logger import get_logger

logger = get_logger("openai_whisper_controller")

class SpeechService(speech_Service_pb2_grpc.SpeechServiceServicer):
    
    def Transcribe(self, request, context):
        logger.info("Transcribe request received - gRPC")
        # request.audio es bytes; aquí invoca tu lógica de Whisper
        result = transcribe(request.audio)
        return speech_Service_pb2.TranscribeResponse(text=result)

    def Analyse(self, request, context):
        logger.info("Analyse request received - gRPC")
        result = analyse(request.audio)
        return speech_Service_pb2.AnalyseResponse(result=result)

    def Ask(self, request, context):
        logger.info(f"Ask request received - gRPC with input length: {len(request.user_input)}")
        response = ask(request.user_input)
        return speech_Service_pb2.AskResponse(response=response)
