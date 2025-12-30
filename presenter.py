import cv2
import time
from datetime import datetime

def presenter(input_queue):
    start_time = time.time()
    frame_count = 0

    while True:
        data = input_queue.get()

        if data is None:
            break

        frame = data["frame"]
        detections = data["detections"]
        frame_count += 1

        for (x, y, w, h) in detections:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        timestamp = datetime.now().strftime("%H:%M:%S")
        cv2.putText(
            frame, timestamp, (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
        )

        cv2.imshow("Video Analytics", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    total_time = time.time() - start_time
    print("\n===== Video Analytics Summary =====")
    print(f"Total frames displayed: {frame_count}")
    print(f"Total runtime: {total_time:.2f} seconds")

    cv2.destroyAllWindows()
