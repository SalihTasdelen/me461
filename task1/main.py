import logging
from time import time
from multiprocessing import Process, Queue
import pygame
from gameEngine.sensors.handSensor import HandSensor
from gameEngine.gameLoop import GameLoop
from gameEngine.config import *

# MP
MAX_QUEUE_SIZE = 256

# Logging
level = logging.INFO
logging.basicConfig(format='%(levelname)s:%(message)s', level=level)

# Frames per Second
FPS_CAP = 60
SPF_CAP = 1 / FPS_CAP


if __name__ == '__main__':
    pygame.init()

    sensor = HandSensor(max_queue_size=256)    
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    gl = GameLoop(sensor, screen, max_fps= FPS_CAP)
    gl.start()

    pygame.quit()
