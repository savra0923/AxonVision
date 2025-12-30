import multiprocessing as mp
from streamer import streamer
from detector import detector
from presenter import presenter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


if __name__ == "__main__":
    mp.set_start_method("spawn")
    shutdown_event = mp.Event()

    video_path = BASE_DIR / "instructions" / "People - 6387.mp4"
    mode = 1

    q1 = mp.Queue(maxsize=10)
    q2 = mp.Queue(maxsize=10)

    p_streamer = mp.Process(target=streamer, args=(video_path, q1, shutdown_event))
    p_detector = mp.Process(target=detector, args=(q1, q2, shutdown_event))
    p_presenter = mp.Process(target=presenter, args=(q2, mode, shutdown_event))

    p_streamer.start()
    p_detector.start()
    p_presenter.start()

    p_streamer.join()
    p_detector.join()
    p_presenter.join()
