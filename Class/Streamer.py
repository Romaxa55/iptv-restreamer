import os
import shutil
import threading
import time
from os import makedirs
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import ffmpeg_streaming
from ffmpeg_streaming import *
import psutil

PROCNAME = "ffmpeg"
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

    @staticmethod
    def create_dash_representations():
        # Create DASH Representations
        return [
            Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024)),
            Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024)),
            Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024)),
            Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024)),
            Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024)),
        ]

    def process_representation(self, video, rep):
        hls = video.hls(Formats.hevc())
        hls.representations(*rep)
        print(rep)
        hls.output(f"{self.tmp}/index.m3u8")

    def runStream(self, stream_id):
        global SIGINT
        global last_time
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
                if Path(f"tmp").exists():
                    shutil.rmtree("tmp")
        print("Start ", stream_id)
        stream = ffmpeg_streaming.input(self.url_path)
        print(stream_id)
        if not os.path.exists(self.tmp):
            makedirs(self.tmp)

        # Process the representations concurrently
        with ThreadPoolExecutor() as executor:
            reps = self.create_dash_representations()

            # Process the first representation
            executor.submit(self.process_representation, stream, reps[:1])

            # Process the other representations concurrently
            executor.submit(self.process_representation, stream, reps[1:])

        print("Stop ", stream_id)
        print(self.tmp)
        # if Path(self.tmp).exists():
        #     shutil.rmtree(self.tmp)
