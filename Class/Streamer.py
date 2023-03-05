import os
import shutil
import threading
import time
from os import makedirs

from vidgear.gears import CamGear
from vidgear.gears import StreamGear

SIGINT = False


class Streamer(object):
    nameThread: str = None

    def __init__(self, **kwargs: dict):
        self.tmp = f"tmp{kwargs['path'][:-10]}"
        self.file = f"tmp{kwargs['path'][-10:]}"
        self.url_path = kwargs['host'] + kwargs['path']
        self.nameThread = kwargs['id'].__str__()
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
        print("Start ", stream_id)
        stream = CamGear(self.url_path).start()
        if not os.path.exists(self.tmp):
            makedirs(self.tmp)
        stream_params = {"-input_framerate": stream.framerate, "-livestream": True}
        streamer = StreamGear(output=f"{self.tmp}/hls_out.m3u8", format="hls", **stream_params)
        while True:
            frame = stream.read()
            if frame is None:
                break
            if SIGINT:
                break
            streamer.stream(frame)
        stream.stop()
        print("Stop ", stream_id)
        print(self.tmp)
        shutil.rmtree(self.tmp)
        streamer.terminate()
