from concurrent import futures
import grpc
from .generated import users_pb2_grpc
from .grpc import UsersSer


class Server:

    @staticmethod
    def run():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        users_pb2_grpc.add_UsersServicer_to_server(UsersSer(), server)
        #к серверу привязывается сервисер (Echoer) с помощью функции регистрации
        server.add_insecure_port("[::]:50051")
        #добавляется порт прослушивания
        server.start()
        server.wait_for_termination()