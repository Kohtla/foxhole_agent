# Скрипт для запуска обучения YOLOv8 на вашем датасете
from ultralytics import YOLO

def train():
    model = YOLO('yolov8n.pt')  # Можно заменить на yolov8s.pt, yolov8m.pt и т.д.
    model.train(
        data='foxhole_data.yaml',
        epochs=200,
        imgsz=640,
        project='runs/train',
        name='foxhole_yolov8',
        exist_ok=True
    )

if __name__ == "__main__":
    train()
