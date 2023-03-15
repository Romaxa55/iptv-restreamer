import os
import shutil
import threading
import time
from os import makedirs
import ffmpeg_streaming
from ffmpeg_streaming import *
from pathlib import Path
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

    def runStream(self, stream_id):
        global SIGINT
        global last_time
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
        print("Start ", stream_id)
        stream = ffmpeg_streaming.input(self.url_path, capture=True)
        print(stream_id)
        if not os.path.exists(self.tmp):
            makedirs(self.tmp)

        _144p = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
        _240p = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
        _360p = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
        _480p = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
        _720p = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
        _1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
        _auto = Representation()
        hls = stream.hls(Formats.hevc())
        # hls.representations(_144p, _240p)
        # hls.representations(_144p, _auto)
        hls.auto_generate_representations()

        hls.output(f"{self.tmp}/index.m3u8")
        print("Stop ", stream_id)
        print(self.tmp)
        # if Path(self.tmp).exists():
        #     shutil.rmtree(self.tmp)
