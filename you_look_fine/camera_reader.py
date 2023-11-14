import threading
import cv2
import numpy as np
import time
from .logger import logger
from .config import config

class CameraReader(threading.Thread):

    # Define the list of class labels MobileNet SSD was trained to detect
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]
    WARM_UP_FRAMES = 100

    def __init__(self, camera_source, motion_threshold, debug=False):
        super().__init__()
        try:
            # Try to convert the camera source to an integer
            camera_source = int(camera_source)
        except ValueError:
            # If it can't be converted to an integer, assume it's an RTSP URL
            pass

        self.camera = cv2.VideoCapture(camera_source)
        self.latest_frame = None
        self.running = True
        self.motion_detector = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=56, detectShadows=False)
        self.net = cv2.dnn.readNetFromCaffe('mobile_net/MobileNetSSD_deploy.prototxt.txt', 'mobile_net/MobileNetSSD_deploy.caffemodel')
        self.motion_threshold = int(motion_threshold)
        self.debug = debug
        self._motion_detected = False
        self.motion_mask = None
        self.detected_features = []

    def run(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                self.latest_frame = frame
                self._motion_detected = self.detect_motion(frame)
                if self.motion_detected:
                    feature_frame = self.detect_features(frame)
                    if self.debug:
                        self.frame_to_display = feature_frame

    def capture_frames(self, num_frames, delay):
        frames = []
        for _ in range(num_frames):
            frame = self.get_latest_frame()
            if frame is not None:
                image_path = f'/tmp/detected_motion_{len(frames)}.jpg'
                cv2.imwrite(image_path, frame)
                frames.append(image_path)
                logger.debug("Frame captured, waiting %d ms", delay)

            time.sleep(delay / 1000)  # convert ms to seconds

        return frames
                            
    def detect_motion(self, frame):
        self.motion_mask = cv2.GaussianBlur(self.motion_detector.apply(frame), (5, 5), 0)
        motion_detected = self.motion_mask.sum() > self.motion_threshold
        return motion_detected

    def detect_features(self, frame):
        self.detected_features = []
        frame_copy = frame.copy()
        (h, w) = frame_copy.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame_copy, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            idx = int(detections[0, 0, i, 1])
            if confidence > 0.2 and self.CLASSES[idx] in ['person', 'car', 'cat', 'dog', 'bird', 'horse', 'sheep', 'cow']:
                self.detected_features.append(self.CLASSES[idx])
                # Draw the prediction on the frame copy
                if self.debug:
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                    cv2.rectangle(frame_copy, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(frame_copy, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame_copy

    def feature_detection_frame(self):
        return self.frame_to_display

    def motion_detected(self):
        return self._motion_detected

    def has_feature(self, *features):
        return any(feature in self.detected_features for feature in features)

    def get_latest_frame(self):
        return self.latest_frame

    def stop(self):
        time.sleep(0.1)
        self.camera.release()
        cv2.destroyAllWindows()
        self.running = False