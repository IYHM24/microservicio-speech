from concurrent import futures
from src.gRPC.stubs import speech_service_pb2_grpc
from src.gRPC.controllers.openai_whisper_controller import SpeechService
from src.gRPC.controllers.health_controller import HealthService
from src.gRPC.stubs import health_pb2_grpc

import grpc
import os

def initGrpc():
    
    port = int(os.getenv("PORT_GRPC", 50051))
    # Crear un servidor gRPC con un pool de hilos para manejar las solicitudes concurrentes
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Registrar el servicio en el servidor gRPC
    health_pb2_grpc.add_HealthServiceServicer_to_server(HealthService(), server)
    speech_service_pb2_grpc.add_SpeechServiceServicer_to_server(SpeechService(), server)
    
    # Iniciar el servidor gRPC en el puerto especificado
    server.add_insecure_port('[::]:'+str(port))
    server.start()
    server.wait_for_termination()