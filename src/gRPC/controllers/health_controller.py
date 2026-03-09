from src.gRPC.stubs import health_pb2, health_pb2_grpc
from src.core.logger import get_logger

logger = get_logger("health_controller")

class HealthService(health_pb2_grpc.HealthServiceServicer):
    def Health(self, request, context):
        logger.info("Health check requested - gRPC")
        return health_pb2.HealthResponse(status="Arriba")