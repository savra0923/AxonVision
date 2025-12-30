import cv2
import time

def streamer(video_path, output_queue, shutdown_event):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = 1.0 / fps if fps > 0 else 1 / 30

    while not shutdown_event.is_set():
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        output_queue.put(frame)

        elapsed = time.time() - start_time
        sleep_time = frame_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    output_queue.put(None)
    cap.release()