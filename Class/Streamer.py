import os
import threading
from os import makedirs

from vidgear.gears import CamGear
from vidgear.gears import StreamGear


class Streamer(object):
    nameThread: str = None

    def __init__(self, **kwargs: dict):
        self.terminate = threading.Event()
        self.tmp = f"tmp{kwargs['path'][:-10]}"
        self.file = f"tmp{kwargs['path'][-10:]}"
        self.url_path = kwargs['host'] + kwargs['path']
        self.nameThread = kwargs['id'].__str__()
        self.runThread()

    def existsThread(self):
        for j in threading.enumerate():
            if self.nameThread in j.name:
                return True

    def runThread(self):
        if not self.existsThread():
            threading.Thread(target=self.runStream,
                             args=[self.terminate],
                             name=self.nameThread,
                             daemon=True).start()
        else:
            print("+" * 100)
            self.terminate.set()
            for thread in threading.enumerate():
                print(thread.name)

    def runStream(self, terminate):
        stream = CamGear(self.url_path).start()
        if not os.path.exists(self.tmp):
            makedirs(self.tmp)
        stream_params = {"-input_framerate": stream.framerate, "-livestream": True}
        streamer = StreamGear(output=f"{self.tmp}/hls_out.m3u8", format="hls", **stream_params)
        while not terminate.is_set():
            frame = stream.read()
            if frame is None:
                break
            streamer.stream(frame)
        stream.stop()
        streamer.terminate()
