from ..mpi.pipe import BindingPipe
from ..mpi.package import Package, PACKAGE_T
from .config import *
from .gameState import GameState
import time
import logging

class PongServer:
    def __init__(self, server: BindingPipe):
        self.server = server
        self.server.listen()
        self.game = GameState()
        self.last_tick = time.time()
    
    def gameLoop(self):

        while self.game.running:
            # time.sleep(0.01)
            current_time = time.time()
            dt = current_time - self.last_tick
            self.last_tick = current_time

            # Handle network messages
            self.handleServer()
            # Update game state
            self.updateGameState(dt)
            # Send updates to clients
            self.sendUpdates()

            self.game.clock.tick(FPS)
    
    def checkPlayers(self):
        # Wait for players!
        if self.server.numOfConnections() < self.server.maxConnection:
            logging.warning('[GAME] Player Connection is lost.')
        
        

    def handleServer(self):
        # self.checkPlayers()

        for i in range(self.server.maxConnection):
            if self.server.available(i) and self.server.receivable(i):
                pkg: Package = self.server.getLastRecv(i)
                if pkg.type == PACKAGE_T.USER_UPDATE:
                    self.game.paddles[i].rect.y = pkg.data * HEIGHT
    
    def updateGameState(self, dt):
        # Update paddles
        for paddle in self.game.paddles:
            paddle.update(dt)

        # Update ball
        self.game.ball.update(dt)

        # Ball and wall collision
        
        if self.game.ball.rect.y < 0:
            self.game.ball.vy = - self.game.ball.vy
            self.game.ball.rect.y = 0
        if self.game.ball.rect.y + self.game.ball.rect.height > HEIGHT:
            self.game.ball.vy = - self.game.ball.vy
            self.game.ball.rect.y = HEIGHT - self.game.ball.rect.height
        
        if self.game.ball.rect.x < 0:
            self.game.ball.vx = - self.game.ball.vx
            self.game.ball.rect.x = 0
        if self.game.ball.rect.x + self.game.ball.rect.width > WIDTH:
            self.game.ball.vx = - self.game.ball.vx
            self.game.ball.rect.x = WIDTH - self.game.ball.rect.width

        # Ball and paddle collision
        for paddle in self.game.paddles:
            if self.game.ball.rect.colliderect(paddle.rect):
                self.game.ball.vx = - self.game.ball.vx
                # self.game.ball.bounce()

        

    def score(self):
        if self.game.ball.rect.left <= 0:
            self.game.scores[1] += 1
        elif self.game.ball.rect.right >= WIDTH:
            self.game.scores[0] += 1

        # Reset the ball and paddles to the starting positions
        self.game.reset()
        return
        # Send the scores to the clients
        for conn in self.connections:
            score_pkg = Package.encode(self.game.scores, PACKAGE_T.SCORE_UPDATE, self.server_port)
            conn.sendQueue.put(score_pkg)

    
    def sendUpdates(self):
        # self.checkPlayers()
        # Send game state to both clients
        for i in range(self.server.maxConnection):
            if self.server.available(i):
                pkg = Package.encode(
                    self.game.getState(i),
                    PACKAGE_T.GAME_TICK,
                    self.server.socket.getsockname()[1]
                )
                self.server.send(i, pkg)
