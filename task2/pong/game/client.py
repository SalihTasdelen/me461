import pygame
from pygame.locals import *
import logging
from ..mpi.pipe import ConnectingPipe
from ..mpi.package import Package, PACKAGE_T
from .config import *
from .gameState import GameState

class PongClient:
    def __init__(self, client: ConnectingPipe, addr, maxDx, maxLagTime):
        self.client = client
        self.addr = addr
        self.client.listen([addr])

        super().__init__()
        self.game = GameState()
        self.firstUpdate = True
        self.maxDx = maxDx

    def gameLoop(self):
        pygame.init()

        while self.game.running:
            # time.sleep(0.02)
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.running = False
                
            if pygame.mouse.get_pressed()[0]:
                y = pygame.mouse.get_pos()[1]
                self.game.paddles[0].setPos(
                    self.game.paddles[0].rect.x,
                    y
                )
                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_UP:
                #         self.game.paddles[0].setPos(WIDTH//2, 100)
                #     if event.key == pygame.K_DOWN:
                #         self.game.paddles[0].setPos(WIDTH//2, 400)
            # Send user input to the server
            self.sendInput()

            # Handle network messages
            self.handleUpdates()

            # Render the game
            self.render()

            self.game.clock.tick(FPS)

    def quit(self):
        pygame.quit()
        self.client.close()
        logging.info('[PONG CLIENT] Quitting.')


    def sendInput(self):
                # Get user input and send it to the server
        y_frac = self.game.paddles[0].rect.y / HEIGHT
        if self.client.available(0):
            pkg = Package.encode(y_frac, PACKAGE_T.USER_UPDATE, self.addr[1])
            self.client.send(0, pkg)

    
    def handleUpdates(self):
        if self.client.available(0) and self.client.receivable(0):
            pkg: Package = self.client.getLastRecv(0)
            if pkg.type == PACKAGE_T.GAME_TICK:
                if abs(self.game.paddles[0].rect.y - pkg.data['ply1'][1]) > self.maxDx:
                    logging.warning('[PONG CLIENT] Input lag detected.')
                if self.firstUpdate:
                    self.firstUpdate = False
                    self.game.setState(pkg.data)
                    return    
                pkg.data['ply1'] = self.game.paddles[0].rect.x, self.game.paddles[0].rect.y
                self.game.setState(pkg.data)
                
                        
    
    def render(self):
        # Clear screen
        self.game.screen.fill((0, 0, 0))

        # Draw paddles and ball
        for paddle in self.game.paddles:
            paddle.draw(self.game.screen)
        self.game.ball.draw(self.game.screen)

        # Update the screen
        pygame.display.flip()
