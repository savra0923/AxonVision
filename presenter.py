import cv2
import time
from datetime import datetime

def blur_gaus(frame, detections):
    for (x, y, w, h) in detections:
        roi = frame[y:y+h, x:x+w]   #get the detection's roi region

        if roi.size == 0:
            continue

        b_roi = cv2.GaussianBlur(roi, (31, 31), 0)
        frame[y:y+h, x:x+w] = b_roi  #inserted the blurred roi into the frame

def presenter(input_queue, mode, shutdown_event):
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
