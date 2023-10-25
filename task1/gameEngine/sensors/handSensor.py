import cv2
import mediapipe as mp
import logging
from multiprocessing import Queue
from ..config import *

class HandSensor:

    def __init__(self, max_queue_size: int = 256) -> None:
        # Sensors own its queues
        self.queue = Queue(maxsize=max_queue_size)

        self.BaseOptions = mp.tasks.BaseOptions
        self.GestureRecognizer = mp.tasks.vision.GestureRecognizer
        self.GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
        self.GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.video = cv2.VideoCapture(0)
        self.timeStamp = 0

        self.options = self.GestureRecognizerOptions(
            # Giving a relative path for the model is not safe.
            base_options=self.BaseOptions(
                model_asset_path='gameEngine/sensors/gesture_recognizer.task'),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            num_hands = MAXNUM_HANDS,
            result_callback=self.resultCallback
        )
        self.resultReady = False
        self.palmCenter = [[0, 0] for _ in range(MAXNUM_HANDS)]
        self.isClosed = [False for _ in range(MAXNUM_HANDS)]
        self.numOfHands = 0
        logging.info(' Hand sensor initialization done.')

    def resultCallback(self,
                       result: mp.tasks.vision.GestureRecognizerResult,
                       output_image: mp.Image, timestamp_ms: int) -> int:

        self.numOfHands = len(result.gestures)
        if not self.numOfHands:
            return
        
        for i in range(len(result.gestures)):
            top_gesture = result.gestures[i][0]
            if top_gesture.category_name != 'Open_Palm':
                self.isClosed[i] = True
            else:
                self.isClosed[i] = False
            
            knuckles = result.hand_landmarks[i]
            if knuckles and len(knuckles) == 21:
                xc, yc = 0, 0
                for j in [0, 5, 9, 13, 17]:
                    xc += knuckles[j].x / 5
                    yc += knuckles[j].y / 5
                self.palmCenter[i][0], self.palmCenter[i][1] = xc * SCREEN_WIDTH, yc * SCREEN_HEIGHT
        
        self.resultReady = True

    def initialize(self):
        self.recognizer = self.GestureRecognizer.create_from_options(self.options)
        return self.recognizer

    def destruct(self):
        self.video.release()
        self.queue.close()

    def detect(self):
        ret, frame = self.video.read()
        # Wait for the camera frame
        if not ret:
            logging.warning(' Ignoring empty frame.')
            return

        self.timeStamp += 1
        frame = cv2.flip(frame, 1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        self.resultReady = False
        self.recognizer.recognize_async(mp_image, self.timeStamp)

        
        # Sync / Wait until result is ready
        # while not self.resultReady:
        #     continue
        
        logging.debug('Hand Landmarker Result:\n{}'.format(self.palmCenter))

        return (self.numOfHands, self.isClosed, self.palmCenter, frame)

    def asyncLoop(self):

        with self.initialize():
            logging.info(' Hand Landmarker Model initialization done.')
            while self.video.isOpened():
                
                result = self.detect()
                if not result:
                    break

                self.queue.put(result)
