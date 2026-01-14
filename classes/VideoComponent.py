class VideoComponent:
    """Base class for all pipeline components."""
    def __init__(self, shutdown_event):
        self.shutdown_event = shutdown_event
        self.process = None

    def start(self):
        """Start the process."""
        self.process.start()

    def join(self):
        """Wait for the process to finish."""
        self.process.join()
