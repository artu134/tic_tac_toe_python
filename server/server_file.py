from concurrent import futures
import time
import grpc

import generated.messages_pb2 as tictactoe_pb2
import generated.messages_pb2_grpc as tictactoe_pb2_grpc

class TicTacToeServicer(tictactoe_pb2_grpc.GameServicer):

    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.players = {}
        self.current_player = 'X'
        self.winner = None

    def Connect(self, request, context):
        player = request.id
        print(f'{player} connected')
        self.players[player] = context
        return tictactoe_pb2.PlayerResponse(
            character=request.character,
            count_players = self.observers.keys().__len__() - 1 <= 0 if 1 else self.observers.keys().__len__() - 1
        )

    def MakeMove(self, request_iterator, context):
        for move_request in request_iterator:
            player = move_request.id
            x, y = move_request.point.x, move_request.point.y

            # Check if game is already over
            if self.winner is not None:
                return tictactoe_pb2.MoveResponse(
                    success=False,
                    message='Game already over! The winner is ' + self.winner
                )

            # Check if valid move
            if self.board[x][y] != ' ':
                return tictactoe_pb2.MoveResponse(
                    success=False,
                    message='Invalid move!'
                )

            # Update board
            self.board[x][y] = self.current_player

            # Check for win condition
            if self._check_win_condition():
                self.winner = self.current_player

            # Update current player
            self.current_player = 'O' if self.current_player == 'X' else 'X'

            # Notify all players of new game state
            response = tictactoe_pb2.MoveResponse(
                success=True,
                message=f'{player} made a move'
            )
            for player, context in self.players.items():
                try:
                    context.write(response)
                    context.flush()
                except Exception:
                    print(f'Error sending update to {player}')

        return tictactoe_pb2.MoveResponse(
            success=True,
            message='Move completed'
        )

    def _check_win_condition(self):
        # Check rows
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return True

        # Check columns
        for i in range(3):
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return True

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True

        return False

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tictactoe_pb2_grpc.add_GameServicer_to_server(TicTacToeServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('Server started. Listening on port 50051...')
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
