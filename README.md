Multi-Process Video Analytics Pipeline
Overview

This project implements a multi-process video analytics pipeline in Python using OpenCV and multiprocessing.

The system consists of three processes:

Streamer: Reads video frames from a file and sends them to the next process via a queue.

Detector: Performs motion detection on the frames, identifies moving objects, and outputs both the original frame and bounding boxes of detected objects.

Presenter: Displays the video frames, optionally applies Gaussian blur to detected regions, and overlays the current time.

The processes communicate via multiprocessing.Queue and can be shut down gracefully with a multiprocessing.Event.

Features

Multi-process architecture: streamer → detector → presenter

Motion detection using frame differencing and contours

Optional blur mode for detected regions

Displays current time on video frames

CLI support for specifying video path and display mode

Graceful shutdown of all processes when video ends or 'q' is pressed

Requirements

Python 3.8+ and the following Python packages are required.

requirements.txt
opencv-python
imutils

Install dependencies
pip install -r requirements.txt

Installation

Clone the repository:

git clone <repository_url>
cd video_pipeline


Install required packages (see above).

Make sure you have a video file in instructions/ (default: People - 6387.mp4).

Running the Program
1. Without CLI arguments (default)

Simply run:

python main.py


Uses the default video file: instructions/People - 6387.mp4

Runs in mode 0 (draw bounding boxes on detections)

2. With CLI arguments
python main.py --video path/to/video.mp4 --mode 1

Argument	Shortcut	Description	Default
--video	-v	Path to the input video file	default instructions/People - 6387.mp4
--mode	-m	Run mode: 0 = draw bounding boxes, 1 = blur detections	0

Example:

python main.py -v instructions/People-6387.mp4 -m 1


This will run the pipeline on the specified video and blur detected regions.

Controls

Press q while the video window is focused to stop the pipeline gracefully.

At the end of the video, all processes terminate automatically.
