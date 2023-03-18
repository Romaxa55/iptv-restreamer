# IPTV Restreamer with Adaptive Streams
![example event parameter](https://github.com/romaxa55/iptv-restreamer/actions/workflows/docker-image.yml/badge.svg?event=push)

This is a Python-based project for IPTV restreaming with adaptive streams. It uses the `python-ffmpeg-video-streaming` package and can be run in a Docker container.

## Run from public repository
`docker run -d --rm -p8000:8000 romaxa55/iptv-restreamer`


## How to Use

1. Clone this repository to your local machine by running `git clone https://github.com/Romaxa55/iptv-restreamer.git`
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Start the restreamer by running `python main.py`
4. Download the playlist from ilook.tv and replace the IP addresses in the m3u8 playlist with your server's IP address and port number (e.g. `http://localhost:8000`).

## Using Docker Build owner image

1. Install Docker on your machine.
2. Build the Docker image by running `docker build -t iptv-restreamer .`
3. Start the Docker container by running `docker run -d --rm -p8000:8000 iptv-restreamer`
4. Download the playlist from [ilook.tv](https://ilook.tv) and replace the IP addresses in the m3u8 playlist with your server's IP address and port number (e.g. `http://localhost:8000`).

## Configuration

The config.json file is used to configure the restreamer. Here is an example configuration:
```json
{
  "webserver": {
    "host": "0.0.0.0",
    "port": 8000
  },
  "iptv": {
    "host": "http://username.otttv.pw"
  }
}
```
You can modify this file to adjust the port number, the path to the playlist, and other settings. By default, the restreamer listens on port 8000.


This program is particularly useful for places with very bad internet connections. The streamer automatically adapts the video quality to your internet channel, ensuring that the streaming is not interrupted due to low bandwidth.

## License

This project is free to use and modify under the MIT License. See the LICENSE file for details.

## Contact

If you have any questions or issues with the project, you can contact the developer on Telegram: @romaxa55.
