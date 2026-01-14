from VideoComponent import VideoComponent
import multiprocessing as mp
import cv2
import time
from datetime import datetime

class Presenter(VideoComponent):
    """Displays frames, draws rectangles or blurs detections, shows current time."""
    def __init__(self, input_queue, mode, shutdown_event):
        super().__init__(shutdown_event)
        self.input_queue = input_queue
        self.mode = mode
        self.process = mp.Process(
            target=type(self).run,
            args=(self,)
        )

    @staticmethod
    def blur_gaus(frame, detections):
        for x, y, w, h in detections:
            roi = frame[y:y+h, x:x+w]
            if roi.size == 0:
                continue
            frame[y:y+h, x:x+w] = cv2.GaussianBlur(roi, (31, 31), 0)

    def run(self):
        frame_count = 0
        start_time = time.time()

        while not self.shutdown_event.is_set():
            data = self.input_queue.get()
            if data is None:
                self.shutdown_event.set()
                break

            frame = data["frame"]
            detections = data["detections"]
            frame_count += 1

            if self.mode == 0:
                for x, y, w, h in detections:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                self.blur_gaus(frame, detections)

            timestamp = datetime.now().strftime("%H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow("Video Analytics", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.shutdown_event.set()
                break

        total_time = time.time() - start_time
        print(f"Total frames displayed: {frame_count}")
        print(f"Total runtime: {total_time:.2f} sec")
        cv2.destroyAllWindows()
