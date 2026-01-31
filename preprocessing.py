import cv2
import numpy as np

def preprocess_image(img: np.ndarray) -> np.ndarray:
    # Цветовая обработка
    processed = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
    processed = cv2.cvtColor(processed, cv2.COLOR_GRAY2RGB)
    # Изменение размера на numpy
    processed = cv2.resize(processed, (1280, 720))
    return processed
