import logging
import grpc
from concurrent import futures
import generated.messages_pb2 as tictactoeserver_pb2
import generated.messages_pb2_grpc as tictactoeserver_pb2_grpc
from generated.messages_pb2 import ConnectionRequest, MoveRequest, Point
from generated.messages_pb2_grpc import GameStub

logger = logging.getLogger(__name__)

class TicTacToeClient():
    def __init__(self, host: str, port: int):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = GameStub(self.channel)

    def connect(self, name: str, stream_observer):
        logger.info(f"Connecting {name} ...")
        request = ConnectionRequest(id=name)
        try:
            self.stub.connect(request, stream_observer)
        except grpc.RpcError as e:
            logger.warning(f"RPC failed: {e.code()} {e.details()}")

    def make_move(self, point: int, id: str, observer):
        move = self.stub.makeMove(observer)
        move_request = MoveRequest(point=Point(x=point//3, y=point%3), id=id)
        move.on_next(move_request)
        move.on_completed()

    def shutdown(self):
        self.channel.close()