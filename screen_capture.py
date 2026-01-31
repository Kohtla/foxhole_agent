import threading
import mss
from preprocessing import preprocess_image
import numpy as np

class ScreenCaptureProcessor:
    def __init__(self, monitor_index=1, resize_to=(400, 225)):
        self.monitor_index = monitor_index
        self.resize_to = resize_to
        self._stop_event = threading.Event()
        self.latest_frame = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._capture_loop, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop_event.set()
        self.thread.join()

    def _capture_loop(self):
        with mss.mss() as sct:
            monitor = sct.monitors[self.monitor_index]
            while not self._stop_event.is_set():
                sct_img = sct.grab(monitor)
                img = np.array(sct_img)
                im_pil = preprocess_image(img)
                with self.lock:
                    self.latest_frame = im_pil.copy()
                self._stop_event.wait(0.2)

    def get_latest_frame(self):
        with self.lock:
            if self.latest_frame is not None:
                return self.latest_frame.copy()
            return None
