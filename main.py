from Class.WebServer import WebServer
# Built-in library
import json

if __name__ == '__main__':
    with open('config.json') as fp:
        cfg = json.load(fp)
    webserver = WebServer(**cfg)
    webserver.run()