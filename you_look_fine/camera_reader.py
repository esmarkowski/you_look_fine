import threading

class CameraReader(threading.Thread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.latest_frame = None
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.camera.read()
            if ret:
                self.latest_frame = frame

    def get_latest_frame(self):
        return self.latest_frame

    def stop(self):
        self.running = False