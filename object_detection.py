from ultralytics import YOLO
import numpy as np

class ObjectDetector:
    def __init__(self, model_path='runs/detect/runs/train/foxhole_yolov8/weights/best.pt'):
        self.model = YOLO(model_path)

    def detect(self, frame: np.ndarray):
        # frame должен быть в формате RGB, размер не критичен (YOLO сам ресайзит)
        results = self.model(frame)
        # results[0].boxes.xyxy, results[0].boxes.conf, results[0].boxes.cls
        return results[0]
