import shutil

from Class.WebServer import WebServer
# Built-in library
import json
from pathlib import Path

if __name__ == '__main__':
    with open('config.json') as fp:
        cfg = json.load(fp)
    if Path(f"tmp").exists():
        shutil.rmtree("tmp")
    webserver = WebServer(**cfg)
    webserver.run()
