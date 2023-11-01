import pygame
from pygame.locals import *
from .config import * 

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 100)
        self.speed = 100

    def update(self, dt):
        pass
        # keys = pygame.key.get_pressed()
        # if keys[K_UP]:
        #     self.rect.move_ip(0, -self.speed * dt)
        # if keys[K_DOWN]:
        #     self.rect.move_ip(0,  self.speed * dt)

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def setRelPos(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.vx = 100
        self.vy = 100

    def update(self, dt):
        self.rect.move_ip(self.vx * dt, self.vy * dt)
        # if self.rect.top < 0 or self.rect.bottom > 500:
        #     self.vy = -self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)