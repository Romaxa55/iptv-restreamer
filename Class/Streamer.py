# import required libraries
import os
from os import makedirs
import threading

from vidgear.gears import CamGear
from vidgear.gears import StreamGear


class Streamer(object):
    def __init__(self, **kwargs: dict):
        self.stream = CamGear(kwargs['host'] + kwargs['path']).start()
        self.tmp = f"tmp{kwargs['path'][:-10]}"
        self.file = f"tmp{kwargs['path'][-10:]}"

        thread = threading.Thread(target=self.runStream, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    async def runStream(self):
        if not os.path.exists(self.tmp):
            makedirs(self.tmp)
        stream_params = {"-input_framerate": self.stream.framerate, "-livestream": True}
        streamer = StreamGear(output=f"{self.tmp}/hls_out.m3u8", format="hls", **stream_params)
        while True:
            frame = self.stream.read()
            if frame is None:
                break
            streamer.stream(frame)
            # if 'index.m3u8' in self.file:
            #     break
        self.stream.stop()
        streamer.terminate()


