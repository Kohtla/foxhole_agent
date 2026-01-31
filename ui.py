import tkinter as tk
from tkinter import ttk
from foxhole_status import is_foxhole_running

from PIL import ImageTk, Image
from screen_capture import ScreenCaptureProcessor


class FoxholeMonitorUI:
    def __init__(self, root, capture_processor: ScreenCaptureProcessor):
        self.root = root
        self.root.title("Foxhole Monitor")
        self.root.attributes("-topmost", True)
        self.status_label = ttk.Label(root, text="Checking...", font=("Arial", 12))
        self.capture_processor = capture_processor
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
            frame_pil = Image.fromarray(frame)
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
