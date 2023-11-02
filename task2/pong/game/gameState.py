import pygame
from .config import *
from .objects import Paddle, Ball


class GameState:
    def __init__(self, serverMode = False):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.paddles = [Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2),
                        Paddle(WIDTH - 30, HEIGHT//2 - PADDLE_HEIGHT//2)]
        self.ball = Ball(WIDTH//2, HEIGHT//2)
        self.running = True

    def reset(self):
        self.__init__()

    def getState(self, i):
        print(f'P1 : {self.paddles[0].rect.y}, P2 : {self.paddles[1].rect.y}')
        if i == 0:
            return [
                self.ball.rect.centerx,
                self.ball.rect.centery,
                self.paddles[0].rect.x,
                self.paddles[0].rect.y,
                self.paddles[1].rect.x,
                self.paddles[1].rect.y,
            ]
        else:
            return [
                self.ball.rect.centerx,
                self.ball.rect.centery,
                self.paddles[1].rect.x,
                self.paddles[1].rect.y,
                self.paddles[0].rect.x,
                self.paddles[0].rect.y,
            ]
    
    def setState(self, data: dict):
        self.ball.rect.centerx = data['ball'][0]
        self.ball.rect.centery = data['ball'][1]
        self.paddles[0].rect.x = 0.1 * self.paddles[0].rect.x + 0.9 * data['ply1'][0]
        self.paddles[0].rect.y = 0.1 * self.paddles[0].rect.y + 0.9 * data['ply1'][1]
        self.paddles[1].rect.x = 0.1 * self.paddles[1].rect.x + data['ply2'][0]
        self.paddles[1].rect.y = 0.1 * self.paddles[1].rect.x + data['ply2'][1]
       
        print(f'P1 : {self.paddles[0].rect.y}, P2 : {self.paddles[1].rect.y}')