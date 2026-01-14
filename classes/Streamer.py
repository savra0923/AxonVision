from VideoComponent import VideoComponent
import multiprocessing as mp
import cv2
import time

class Streamer(VideoComponent):
    """Reads frames from a video file and sends them to a queue."""
    def __init__(self, video_path, output_queue, shutdown_event):
        super().__init__(shutdown_event)
        self.video_path = video_path
        self.output_queue = output_queue
        self.process = mp.Process(
            target=type(self).run,
            args=(self,)
        )

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            print(f"[Streamer] ERROR: cannot open video file: {self.video_path}")
            self.output_queue.put(None)
            return
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = 1.0 / fps if fps > 0 else 1 / 30

        while not self.shutdown_event.is_set():
            start_time = time.time()
            ret, frame = cap.read()
            if not ret:
                break
            self.output_queue.put(frame)
            elapsed = time.time() - start_time
            time.sleep(max(0, frame_interval - elapsed))

        self.output_queue.put(None)
        cap.release()
