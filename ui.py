import tkinter as tk
from tkinter import ttk
from foxhole_status import is_foxhole_running

from PIL import ImageTk, Image, ImageDraw
from screen_capture import ScreenCaptureProcessor

from object_detection import ObjectDetector
from preprocessing import preprocess_image
from foxhole_classes import CLASS_NAMES


class FoxholeMonitorUI:
    def __init__(self, root, capture_processor: ScreenCaptureProcessor):
        self.root = root
        self.root.title("Foxhole Monitor")
        self.root.attributes("-topmost", True)
        self.status_label = ttk.Label(root, text="Checking...", font=("Arial", 12))
        self.capture_processor = capture_processor
        self.detector = ObjectDetector()  # YOLOv8n по умолчанию
        self.status_label.pack(padx=20, pady=10)
        self.strategy_label = ttk.Label(
            root, text="Strategies:", font=("Arial", 14, "bold")
        )
        self.strategy_label.pack(padx=20, pady=(10, 0))
        self.run_circle_active = False
        self.run_circle_btn = ttk.Button(
            root, text="Run in Circle", command=self.toggle_run_in_circle
        )
        self.run_circle_btn.pack(padx=20, pady=5)

        # Label for displaying the image
        self.image_label = ttk.Label(root)
        self.image_label.pack(padx=20, pady=10)
        self.current_image = None
        # Экземпляр ScreenCaptureProcessor должен передаваться извне
        self.update_image_loop()
        self.update_status()

    def toggle_run_in_circle(self):
        import threading
        from strategies import start_run_in_circle, stop_run_in_circle

        if not self.run_circle_active:
            self.run_circle_active = True
            self.run_circle_btn.config(text="Stop Run in Circle")
            threading.Thread(target=start_run_in_circle, daemon=True).start()
        else:
            self.run_circle_active = False
            self.run_circle_btn.config(text="Run in Circle")
            stop_run_in_circle()

    def update_status(self):
        running = is_foxhole_running()
        status_text = "🟢 Foxhole running" if running else "❌ Foxhole not running"
        self.status_label.config(text=status_text)
        self.run_circle_btn.config(state=tk.NORMAL if running else tk.DISABLED)
        # If game is not running, stop strategy and reset button
        if not running and self.run_circle_active:
            self.run_circle_active = False
            self.run_circle_btn.config(text="Run in Circle")
            from strategies import stop_run_in_circle

            stop_run_in_circle()
        self.root.after(1000, self.update_status)

    def update_image_loop(self):
        frame = self.capture_processor.get_latest_frame()
        if frame is not None:
            # Анализ кадра нейросетью
            processed = preprocess_image(frame)
            results = self.detector.detect(processed)
            # Визуализация боксов
            frame_pil = Image.fromarray(processed)
            draw = ImageDraw.Draw(frame_pil)
            if hasattr(results, 'boxes') and results.boxes is not None:
                boxes = results.boxes.xyxy.cpu().numpy() if hasattr(results.boxes.xyxy, 'cpu') else results.boxes.xyxy
                confs = results.boxes.conf.cpu().numpy() if hasattr(results.boxes.conf, 'cpu') else results.boxes.conf
                clss = results.boxes.cls.cpu().numpy() if hasattr(results.boxes.cls, 'cpu') else results.boxes.cls
                for box, conf, cls in zip(boxes, confs, clss):
                    x1, y1, x2, y2 = map(int, box)
                    class_name = CLASS_NAMES[int(cls)] if int(cls) < len(CLASS_NAMES) else str(int(cls))
                    draw.rectangle([x1, y1, x2, y2], outline='white', width=1)
                    draw.text((x1, y1), f'{class_name} {conf:.2f}', fill='white')
            frame_pil = frame_pil.resize((640, 360))
            imgtk = ImageTk.PhotoImage(image=frame_pil)
            self.update_image(imgtk)
        self.root.after(200, self.update_image_loop)

    def update_image(self, imgtk):
        self.current_image = imgtk  # Keep a reference to prevent GC
        self.image_label.config(image=imgtk)


if __name__ == "__main__":
    root = tk.Tk()
    app = FoxholeMonitorUI(root)
    root.mainloop()
