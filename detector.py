import cv2
import imutils

def detector(input_queue, output_queue, shutdown_event):
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