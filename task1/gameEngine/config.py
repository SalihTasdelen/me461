# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_HEIGHT = 200
SPEED = 5
VANISHING_POINT_Y = SCREEN_HEIGHT/2
VANISHING_POINT_X = SCREEN_WIDTH / 2
MAXNUM_HANDS = 2

# How many frames between spawning a new tile
SPAWN_INTERVAL = 0.5* TILE_HEIGHT / SPEED 

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Transparency
TRANSPARENCY = 128

# Image List
IMAGE_PATH = 'gameEngine/sprites/'
IMAGES = [
    'bugra.jpg',
    'aliemre.jpg',
    'rsppi.png',
    'python.png',
    'bash.png',
    'tux.png',
    'win.png',
    'vim.png',
    'vscode.png'
]

# Score Points
POINTS = [
    10,
    -10,
    5,
    1,
    3,
    6,
    -6,
    3,
    -3
]