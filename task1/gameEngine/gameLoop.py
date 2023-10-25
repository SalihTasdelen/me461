import pygame
from multiprocessing import Process
from time import time
import logging

from .config import *
from .sensors.handSensor import HandSensor
from .objects import Tile, Button

# Will be removed
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

class GameLoop:

    def __init__(self, sensor: HandSensor, screen: pygame.Surface, max_fps) -> None:
        self.sensor = sensor
        self.screen = screen
        # Fonts
        self.font = pygame.font.Font(None, 74)

        self.objects = []
        self.gameOver = False
        self.score = 0
        self.frames_since_last_spawn = 0

        # Define the async loop process for the sensor
        self.sensorProc = Process(target=sensor.asyncLoop)

        self.running = True
        self.spf = 1.0 / max_fps

    def start(self):
        # Start the sensor loop
        self.sensorProc.start()
        
        running = True
        t0 = time()

        # Here for the demo will be removed
        HEIGHT = self.screen.get_height()
        WIDTH = self.screen.get_width()

        self.objects.append(Tile.randomTile(self.screen))

        while running:

            t1 = time()
            if t1 - t0 < self.spf:
                continue

            # logging.info(f' FPS: {(1 / (t1 - t0)):4.2f}')
            t0 = t1

            for event in pygame.event.get():
                # Keyboard events will be here
                if event.type == pygame.QUIT:
                    running = False

            # logging.info(f' Queue Size: {self.sensor.queue.qsize()}')

            # # If no input skip just like the pygame events
            if self.sensor.queue.qsize() == 0:
                continue
            
            # # Get the last event ignore rest
            for _ in range(self.sensor.queue.qsize()):
                self.numOfHands, self.isClosedList, self.centerList, frame = self.sensor.queue.get()

            # Convert camera frame & rescale
            camera_frame = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "BGR")
            camera_frame = pygame.transform.scale(camera_frame, (WIDTH, HEIGHT))
            camera_frame.set_alpha(TRANSPARENCY)

            # Reset Screen
            self.screen.fill(GRAY)
            self.screen.blit(camera_frame, (0, 0))

            if not self.gameOver:
                if self.numOfHands > 0:
                    # Pointer Update
                    for i in range(self.numOfHands):
                        color = RED if self.isClosedList[i] else BLUE
                        rect = pygame.Rect(
                            self.centerList[i][0] - 20, 
                            self.centerList[i][1] - 20,
                            40, 40)
                        pygame.draw.rect(self.screen, color, rect)

                for obj in self.objects:
                    obj.update()

                self.collisionDetection()

                for obj in self.objects:
                    obj.draw()

                self.drawScoreBoard()

                # Tile Generation
                self.frames_since_last_spawn += 1
                if self.frames_since_last_spawn >= SPAWN_INTERVAL:
                    self.objects.append(Tile.randomTile(self.screen))
                    self.frames_since_last_spawn = 0

            else:
                restartButton = self.drawGameOverScreen()
                if restartButton.is_clicked():
                    # Reset game state
                    self.objects.clear()
                    self.objects.append(Tile.randomTile(self.screen))
                    self.score = 0
                    self.gameOver = False
                    self.frames_since_last_spawn = 0


            # Update the display
            pygame.display.flip()
        
        # Kill the sensor process
        self.sensorProc.kill()
        self.sensor.destruct()


    def collidePoint(self, flag, position):
        if flag:
            for obj in self.objects:
                collided = obj.collide(position)
                print('collided')
                if collided:
                    self.objects.remove(obj)
                    self.score += obj.score

    def collisionDetection(self):
        # Mouse Input
        mousePressed = pygame.mouse.get_pressed()[0]
        mousePos = pygame.mouse.get_pos()

        self.collidePoint(mousePressed, mousePos)

        for i in range(self.numOfHands):
            print(self.isClosedList[i], self.centerList[i])
            self.collidePoint(self.isClosedList[i], self.centerList[i])

        # Screen bounds
        for obj in self.objects:
            if obj.rect.top + obj.rect.height >= SCREEN_HEIGHT:
                if obj.score < 0:
                    self.objects.remove(obj)
                else:
                    self.gameOver = True
        
        return

    def drawGameOverScreen(self):
        textList = ['Game Over!', f'Score: {self.score}']
        prevHeights = -100 # Start 100px above center
        for i in range(len(textList)):
            text = self.font.render(textList[i], True, RED)
            self.screen.blit(text,
                (SCREEN_WIDTH / 2 - text.get_width() / 2,
                SCREEN_HEIGHT / 2 - text.get_height() / 2 + prevHeights)
            )
            prevHeights += text.get_height()
        restart_button = Button(
            self.screen,
            self.font,
            SCREEN_WIDTH / 2 - 100,
            SCREEN_HEIGHT / 2 + prevHeights,
            200, 75, GRAY, "Restart")
        restart_button.draw()
        return restart_button
        
    def drawScoreBoard(self):
        score_text = self.font.render("Score: " + str(self.score), True, RED)
        self.screen.blit(score_text, (10, 10))
        