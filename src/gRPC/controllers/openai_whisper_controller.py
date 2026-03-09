
from gRPC import speech_service_pb2, speech_service_pb2_grpc

class SpeechService(speech_service_pb2_grpc.SpeechServiceServicer):
    def Transcribe(self, request, context):
        # request.audio es bytes; aquí invoca tu lógica de Whisper
        text = "transcripción de ejemplo"
        return speech_service_pb2.TranscribeResponse(text=text)

    def Analyse(self, request, context):
        result = "análisis de ejemplo"
        return speech_service_pb2.AnalyseResponse(result=result)

    def Ask(self, request, context):
        response = "respuesta del LLM"
        return speech_service_pb2.AskResponse(response=response)
