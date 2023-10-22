import pygame
from .sensors.handSensor import HandSensor
from multiprocessing import Process
from time import time
import logging

# Will be removed
BLUE = (0, 0, 255)
GRAY = (150, 150, 150)

class GameLoop:

    def __init__(self, sensor: HandSensor, screen: pygame.Surface, max_fps) -> None:
        self.sensor = sensor
        self.screen = screen

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

        # Just an example rectangle
        # Must become an object which has an update and a render function
        rect = pygame.Rect(WIDTH/2, HEIGHT/2, 80, 80)

        while running:

            t1 = time()
            if t1 - t0 < self.spf:
                continue

            logging.info(f' FPS: {(1 / (t1 - t0)):4.2f}')
            t0 = t1

            for event in pygame.event.get():
                # Keyboard events will be here
                if event.type == pygame.QUIT:
                    running = False

            logging.info(f' Queue Size: {self.sensor.queue.qsize()}')

            # If no input skip just like the pygame events
            if self.sensor.queue.qsize() == 0:
                continue
            
            # Get the last event ignore rest
            for _ in range(self.sensor.queue.qsize()):
                center, frame = self.sensor.queue.get()

            # Convert camera frame & rescale
            camera_frame = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1], "BGR")
            camera_frame = pygame.transform.scale(camera_frame, (WIDTH, HEIGHT))

            # Reset Screen
            self.screen.fill(GRAY)
            self.screen.blit(camera_frame, (0, 0))

            # Dunno which to add and subtract
            rect.update(
                (center[0] * WIDTH - rect.width / 2, 
                 center[1] * HEIGHT - rect.height / 2),
                (rect.width, rect.height)
            )
            pygame.draw.rect(self.screen, BLUE, rect)

            # Update the display
            pygame.display.flip()
        
        # Kill the sensor process
        self.sensorProc.kill()
        self.sensor.destruct()
        

        