import cv2
import imutils

def detector(input_queue, output_queue, shutdown_event):
    """
    Detect motion in video frames received from an input queue and send results to the output queue.

    This function continuously receives frames from the input queue, performs basic motion
    detection by comparing consecutive frames, and outputs both the original frame and a list
    of detected bounding boxes representing moving objects. The function stops when it receives
    a sentinel `None` or when the shutdown_event is set.

    Args:
        input_queue (multiprocessing.Queue): Queue from which frames are received (from the streamer).
        output_queue (multiprocessing.Queue): Queue to send processed frames and detections to the next process.
        shutdown_event (multiprocessing.Event): Event used to signal early termination of the process.

    Behavior:
        - Converts each frame to grayscale.
        - Compares the current frame with the previous frame using absolute difference.
        - Thresholds and dilates the difference to highlight areas of motion.
        - Finds contours corresponding to moving objects.
        - Filters out small contours (less than 500 pixels) to reduce false positives.
        - Outputs a dictionary containing:
            - "frame": the original frame
            - "detections": a list of bounding boxes [(x, y, w, h), ...] for moving objects
        - Sends `None` to the output queue if input frame is `None`.
    """

    prev_frame = None
    counter = 0

    while not shutdown_event.is_set():
        frame = input_queue.get()

        if frame is None:
            output_queue.put(None)
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = []

        if counter == 0:
            prev_frame = gray_frame
            counter += 1
        else:
            diff = cv2.absdiff(gray_frame, prev_frame)
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

            prev_frame = gray_frame
            counter += 1

        data = {
            "frame": frame,
            "detections": detections
        }
        output_queue.put(data)