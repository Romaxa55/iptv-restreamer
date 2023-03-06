import os
import shutil
import threading
import time
from os import makedirs
from vidgear.gears import CamGear, WriteGear
from vidgear.gears import StreamGear
from pathlib import Path

SIGINT = False
last_time = time.time()
TIMEOUT_NON_ACTIVE = 60


class Streamer(object):
    nameThread: str = None

    def __init__(self, **kwargs: dict):
        global last_time
        self.tmp = f"tmp{kwargs['path'][:-10]}"
        self.file = f"tmp{kwargs['path'][-10:]}"
        self.url_path = kwargs['host'] + kwargs['path']
        self.nameThread = kwargs['id'].__str__()
        last_time = time.time()
        self.runThread()

    def existsThread(self):
        for j in threading.enumerate():
            if self.nameThread in j.name:
                return True

    @staticmethod
    def sendSignal():
        global SIGINT
        SIGINT = not SIGINT

    def runThread(self):
        global SIGINT
        if not self.existsThread():

            try:
                self.sendSignal()
                threading.Thread(target=self.runStream,
                                 args=([self.nameThread]),
                                 name=self.nameThread,
                                 daemon=True).start()
                time.sleep(1)
                self.sendSignal()
            except BaseException as e:
                print(e)

    def runStream(self, stream_id):
        global SIGINT
        global last_time
        print("Start ", stream_id)
        stream = CamGear(self.url_path, logging=True, time_delay=0).start()
        if not os.path.exists(self.tmp):
            makedirs(self.tmp)

        stream_params = {
            "-streams": [
                {"-resolution": "1280x720", "-video_bitrate": "1000k"},
                {"-resolution": "1280x720", "-video_bitrate": "256k"},
                         ],
            "-input_framerate": stream.framerate,
            "-livestream": True
        }

        streamer = StreamGear(output=f"{self.tmp}/hls_out.m3u8", format="hls", **stream_params, logging=False)

        while True:
            frame = stream.read()
            if frame is None:
                break
            if SIGINT or int(time.time() - last_time) >= TIMEOUT_NON_ACTIVE:
                break
            streamer.stream(frame)

        stream.stop()
        print("Stop ", stream_id)
        print(self.tmp)
        if Path(self.tmp).exists():
            shutil.rmtree(self.tmp)
        streamer.terminate()
