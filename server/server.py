from concurrent import futures
import logging
import grpc
import generated.messages_pb2 as tictactoeserver_pb2
import generated.messages_pb2_grpc as tictactoeserver_pb2_grpc

from server.game import Game

class TicTacToeServer(tictactoeserver_pb2_grpc.GameServicer):

    def __init__(self):
        self.game = Game()
        self.observers = dict()

    def connect(self, request, context):
        user_id = request.id
        self.observers[user_id] = context
        logging.info(f"Connecting user: {request.id}")
        self.game.newPlayer(request.id)
        response = tictactoeserver_pb2.PlayerResponse()
        response.count_players = self.observers.keys().__len__() - 1 <= 0 if 1 else self.observers.keys().__len__() - 1
        return response

    def makeMove(self, request_iterator, context):
        for move_request in request_iterator:
            character = self.game.makeMove(move_request.id, move_request.point)
            if character == tictactoeserver_pb2.Character.Value('UNRECOGNIZED'):
                logging.warning(f"Wrong point for {move_request.point}")
                context.set_details('Invalid move')
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return tictactoeserver_pb2.MoveResponse(success=False)
            player_response = tictactoeserver_pb2.PlayerResponse()
            player_response.char = character
            player_response.point.x = move_request.point.x
            player_response.point.y = move_request.point.y
            
            for val, observer in self.observers.items():
                observer.send(player_response)
            if self.game.isFinished():
                for val, observer in self.observers.items():
                    observer.send(None)
                self.game.reset()
            return tictactoeserver_pb2.MoveResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tictactoeserver_pb2_grpc.add_GameServicer_to_server(TicTacToeServer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Server started, listening on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()