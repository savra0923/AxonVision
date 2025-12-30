import multiprocessing as mp
from streamer import streamer
from detector import detector
from presenter import presenter

if __name__ == "__main__":
    mp.set_start_method("spawn")

    video_path = r"C:\Users\Sapir\PycharmProjects\AxonVision\People - 6387.mp4"
    mode = 0

    q1 = mp.Queue(maxsize=10)
    q2 = mp.Queue(maxsize=10)

    p_streamer = mp.Process(target=streamer, args=(video_path, q1))
    p_detector = mp.Process(target=detector, args=(q1, q2))
    p_presenter = mp.Process(target=presenter, args=(q2, mode))

    p_streamer.start()
    p_detector.start()
    p_presenter.start()

    p_streamer.join()
    p_detector.join()
    p_presenter.join()
