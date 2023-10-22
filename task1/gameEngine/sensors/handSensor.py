import cv2
import mediapipe as mp
import logging
import numpy as np
from multiprocessing import Queue


class HandSensor:

    def __init__(self, max_queue_size: int = 256) -> None:
        # Sensors own its queues
        self.queue = Queue(maxsize=max_queue_size)

        self.BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        self.HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        self.HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
        self.VisionRunningMode = mp.tasks.vision.RunningMode

        self.video = cv2.VideoCapture(0)
        self.timeStamp = 0

        self.options = self.HandLandmarkerOptions(
            # Giving a relative path for the model is not safe.
            base_options=self.BaseOptions(
                model_asset_path='gameEngine/sensors/hand_landmarker.task'),
            running_mode=self.VisionRunningMode.LIVE_STREAM,
            result_callback=self.resultCallback
        )
        self.result = None
        self.palmCenter = np.zeros((2,))
        logging.info(' Hand sensor initialization done.')

    def resultCallback(self,
                       result: mp.tasks.vision.HandLandmarkerResult,
                       output_image: mp.Image, timestamp_ms: int) -> int:

        knuckles = None
        if result.hand_landmarks:
            knuckles = result.hand_landmarks[0]

        if knuckles and len(knuckles) == 21:
            xc, yc = 0, 0
            for i in [0, 5, 9, 13, 17]:
                xc += knuckles[i].x / 5
                yc += knuckles[i].y / 5
            self.palmCenter[0], self.palmCenter[1] = xc, yc
        self.result = result

    def initialize(self):
        self.recognizer = self.HandLandmarker.create_from_options(self.options)
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
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        self.result = None
        self.recognizer.detect_async(mp_image, self.timeStamp)

        # Sync / Wait until result is ready
        while not self.result:
            continue

        logging.debug('Hand Landmarker Result:\n{}'.format(self.result))

        return (self.result, frame)

    def asyncLoop(self):

        with self.initialize():
            logging.info(' Hand Landmarker Model initialization done.')
            while self.video.isOpened():
                
                result = self.detect()
                if not result:
                    break

                self.queue.put((self.palmCenter, result[1]))
