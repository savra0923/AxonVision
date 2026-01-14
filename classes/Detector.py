import imutils
from VideoComponent import VideoComponent
import multiprocessing as mp
import cv2
import numpy as np
from scipy.ndimage import binary_dilation
from scipy.ndimage import label


class Detector(VideoComponent):
    """Detects motion in frames received from input_queue and sends results to output_queue."""
    def __init__(self, input_queue, output_queue, shutdown_event):
        super().__init__(shutdown_event)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.process = mp.Process(
            target=type(self).run,
            args=(self,)
        )

    def detect_motion_numpy(self, frame, prev_gray, threshold=25, min_area=500):
        gray = np.mean(frame, axis=2).astype(np.uint8)

        if prev_gray is None:
            return gray, []

        diff = np.abs(gray.astype(np.int16) - prev_gray.astype(np.int16))
        mask = diff > threshold

        labeled, num_objects = label(mask)
        detections = []

        for obj_id in range(1, num_objects + 1):
            ys, xs = np.where(labeled == obj_id)
            if len(xs) < min_area:
                continue

            x_min, x_max = xs.min(), xs.max()
            y_min, y_max = ys.min(), ys.max()

            detections.append(
                (x_min, y_min, x_max - x_min, y_max - y_min)
            )

        return gray, detections

    def run_2(self):
        prev_gray = None

        while not self.shutdown_event.is_set():
            frame = self.input_queue.get()
            if frame is None:
                self.output_queue.put(None)
                break

            gray, detections = self.detect_motion_numpy(frame, prev_gray)
            prev_gray = gray

            self.output_queue.put({
                "frame": frame,
                "detections": detections
            })

    def run(self):
        prev_frame = None
        counter = 0

        while not self.shutdown_event.is_set():
            frame = self.input_queue.get()
            if frame is None:
                self.output_queue.put(None)
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            detections = []

            if counter == 0:
                prev_frame = gray
                counter += 1
            else:
                diff = cv2.absdiff(gray, prev_frame)
                thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
                thresh = cv2.dilate(thresh, None, iterations=2)

                cnts = cv2.findContours(
                    thresh.copy(),
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE
                )
                cnts = imutils.grab_contours(cnts)

                for cnt in cnts:
                    if cv2.contourArea(cnt) < 500:
                        continue
                    x, y, w, h = cv2.boundingRect(cnt)
                    detections.append((x, y, w, h))

                prev_frame = gray
                counter += 1

            self.output_queue.put({"frame": frame, "detections": detections})
