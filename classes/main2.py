import multiprocessing as mp
from Streamer import Streamer
from Detector import Detector
from Presenter import Presenter
from pathlib import Path
import argparse

BASE_DIR = Path(__file__).resolve().parent.parent

def parse_args():
    """
    Parse command line arguments for the video analytics pipeline.

    Returns:
        argparse.Namespace: Parsed arguments with attributes:
            - video (str or None): Path to the input video file. Defaults to None.
            - mode (int): Run mode of the pipeline (0=boxes, 1=blur). Defaults to 0.
    """

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

    shutdown_event = mp.Event()
    q1 = mp.Queue(maxsize=10)
    q2 = mp.Queue(maxsize=10)

    video_path = BASE_DIR / "instructions" / "People - 6387.mp4"
    video_path = str(video_path)
    mode = 0  # 0 = boxes, 1 = blur

    streamer = Streamer(video_path, q1, shutdown_event)
    detector = Detector(q1, q2, shutdown_event)
    presenter = Presenter(q2, mode, shutdown_event)

    streamer.start()
    detector.start()
    presenter.start()

    streamer.join()
    detector.join()
    presenter.join()

