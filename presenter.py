import cv2
import time
from datetime import datetime

def blur_gaus(frame, detections):
    """
    Apply Gaussian blur to all detected regions in a video frame.

    Args:
        frame (numpy.ndarray): The input video frame in BGR format.
        detections (list of tuples): List of bounding boxes for detected objects,
                                    each in the form (x, y, w, h).

    Behavior:
        - Iterates over each detection.
        - Extracts the Region of Interest (ROI) corresponding to the bounding box.
        - Skips the ROI if its size is zero (empty).
        - Applies Gaussian blur with a kernel size of (31, 31) to the ROI.
        - Inserts the blurred ROI back into the original frame.
    """

    for (x, y, w, h) in detections:
        roi = frame[y:y+h, x:x+w]   #get the detection's roi region

        if roi.size == 0:
            continue

        b_roi = cv2.GaussianBlur(roi, (31, 31), 0)
        frame[y:y+h, x:x+w] = b_roi  #inserted the blurred roi into the frame

def presenter(input_queue, mode, shutdown_event):
    """
    Display video frames with detections, optionally applying blur, and overlay the current time.

    Args:
        input_queue (multiprocessing.Queue): Queue from which processed frames and detections are received.
        mode (int): Display mode:
                    0 = draw bounding boxes on detections
                    1 = blur detected regions
        shutdown_event (multiprocessing.Event): Event used to signal early termination of the process.

    Behavior:
        - Continuously receives frames from the input queue.
        - Stops gracefully when it receives None or when shutdown_event is set.
        - Increments frame count for each processed frame.
        - If mode=0, draws green rectangles around detections.
        - If mode=1, applies Gaussian blur to each detection using `blur_gaus`.
        - Overlays the current time (HH:MM:SS) on the top-left corner of the frame.
        - Displays the frame in a window named "Video Analytics".
        - Pressing 'q' will set the shutdown_event and exit.
        - Prints a summary of total frames displayed and total runtime when finished.
    """

    start_time = time.time()
    frame_count = 0

    while not shutdown_event.is_set():
        data = input_queue.get()

        if data is None:
            shutdown_event.set()
            break

        frame = data["frame"]
        detections = data["detections"]
        frame_count += 1

        # if mode is 0 do not blur. if it is 1, blur.
        if not mode:
            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            blur_gaus(frame, detections)

        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(
            frame, timestamp, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )

        cv2.imshow("Video Analytics", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            shutdown_event.set()
            break

    total_time = time.time() - start_time
    print("\n===== Video Analytics Summary =====")
    print(f"Total frames displayed: {frame_count}")
    print(f"Total runtime: {total_time:.2f} seconds")

    cv2.destroyAllWindows()
