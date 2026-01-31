from ui import FoxholeMonitorUI
import tkinter as tk
from screen_capture import ScreenCaptureProcessor

if __name__ == "__main__":
    capture_processor = ScreenCaptureProcessor()
    capture_processor.start()
    root = tk.Tk()
    app = FoxholeMonitorUI(root, capture_processor)
    root.mainloop()
