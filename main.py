import multiprocessing as mp
from streamer import streamer
from detector import detector
from presenter import presenter
from pathlib import Path
import argparse

BASE_DIR = Path(__file__).resolve().parent

def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-process video analytics pipeline"
    )

    parser.add_argument(
        "--video", "-v",
        type=str,
        default=None,
        help="Path to input video file"
    )

    parser.add_argument(
        "--mode", "-m",
        type=int,
        default=0,
        choices=[0, 1],
        help="Run mode (e.g., 0=boxes, 1=blur)"
    )

    return parser.parse_args()

if __name__ == "__main__":
    mp.set_start_method("spawn")

    mode = 0
    video_path = BASE_DIR / "instructions" / "People - 6387.mp4"

    args = parse_args()
    shutdown_event = mp.Event()

    if args.video:
        video_path = Path(args.video)
        if not video_path.is_absolute():
            video_path = BASE_DIR / video_path

    if args.mode:
        mode = args.mode

    video_path = str(video_path)

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
