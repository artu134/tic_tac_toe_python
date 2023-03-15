import logging
import uuid
from grpc import RpcError
import generated.messages_pb2 as tictactoe_pb2
import generated.messages_pb2_grpc as tictactoe_pb2_grpc
from generated.messages_pb2 import ConnectionRequest, MoveRequest, Point
from generated.messages_pb2_grpc import GameStub
from concurrent.futures import ThreadPoolExecutor
import threading

class GameComponent:
    def __init__(self):
        self.map = {i: ' ' for i in range(9)}
        self.client = GameStub(ThreadPoolExecutor(max_workers=1))
        self.user = str(uuid.uuid4())

        self.draw_board()

        threading.Thread(target=self.connect_to_server, daemon=True).start()

    def connect_to_server(self):
        try:
            responses = self.client.connect(iter([ConnectionRequest(id=self.user)]))
            threading.Thread(target=self.handle_updates, args=(responses,), daemon=True).start()
        except RpcError as e:
            logging.error(e)
        
    def handle_updates(self, responses):
        for response in responses:
            point = response.point
            p = point.y + point.x + 2 * point.x
            print(f'{response.char} move to {p}')
            self.map[p] = response.char
            self.draw_board()

    def draw_board(self):
        for i in range(9):
            if i % 3 == 0:
                print('---+---+---')
            print(f' {self.map[i]} ', end='|' if i % 3 < 2 else '\n')
        print('---+---+---')

    def run(self):
        self.connect_to_server()

        while True:
            point = int(input('Enter your move (0-8): '))
            x, y = divmod(point, 3)
            try:
                response = self.client.makeMove(MoveRequest(point=Point(x=x, y=y), id=self.user))                
                if response.success:
                    print('Move successful')
                else:
                    print('Move not allowed')
            except RpcError as e:
                logging.error(e) 

if __name__ == '__main__':
    game = GameComponent()
    game.run()