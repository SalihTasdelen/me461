import pygame
import random
from .config import *

class Button:
    def __init__(self, screen, font, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.screen = screen
        self.font = font
        

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, WHITE)
        self.screen.blit(text_surface, (self.rect.x + self.rect.width / 2 - text_surface.get_width() / 2,
                                   self.rect.y + self.rect.height / 2 - text_surface.get_height() / 2))

    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
    
class Tile:
    def __init__(self, screen, col, y, tType):
        self.col = col
        self.y = y
        self.calculate_rect()
        self.screen = screen
        self.score = POINTS[tType]
        self.img = pygame.image.load(IMAGE_PATH + IMAGES[tType])

    def calculate_rect(self):
        distance_factor = (self.y - VANISHING_POINT_Y) / (SCREEN_HEIGHT - VANISHING_POINT_Y)
        width = SCREEN_WIDTH / 4 * (1 + distance_factor)
        height = TILE_HEIGHT * (1 + distance_factor)
        x = self.col * SCREEN_WIDTH / 4 - (width - SCREEN_WIDTH / 4) / 2
        self.rect = pygame.Rect(x, self.y, width, height)

    def update(self):
        self.y += SPEED
        self.calculate_rect()

    def draw(self):
        # pygame.draw.rect(self.screen, BLACK, self.rect)
        img = pygame.transform.scale(self.img,
            (self.rect.width, self.rect.height)
        )
        self.screen.blit(img, self.rect)

    def collide(self, position):
        collided = self.rect.collidepoint(position)
        return collided

    @staticmethod
    def drawTiles(tiles):
        for tile in tiles:
            tile.draw()

    @staticmethod
    def randomTile(screen):
        tType = random.randint(0, len(IMAGES) - 1)
        col = random.randint(0, 3)
        tile = Tile(screen, col, 0, tType)
        return tile
    