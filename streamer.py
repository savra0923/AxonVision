import cv2
import time

def streamer(video_path, output_queue, shutdown_event):
    """
    Stream video frames from a file and send them to the output queue at the original FPS.

    This function reads a video file frame by frame and puts each frame into a multiprocessing
    queue for downstream processes (e.g., detector). The streaming respects the video's original
    FPS by introducing sleep intervals between frames. The function terminates gracefully when
    the video ends or when the shutdown_event is set.

    Args:
        video_path (str): Path to the input video file.
        output_queue (multiprocessing.Queue): Queue to send frames to the next process.
        shutdown_event (multiprocessing.Event): Event used to signal early termination of the process.

    Behavior:
        - Reads video frames using OpenCV.
        - Maintains the original frame rate by calculating sleep intervals.
        - Puts `None` into the output queue when the video ends to signal downstream processes.
        - Releases the video capture object on exit.
    """

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