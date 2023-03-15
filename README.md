# IPTV Restreamer with Adaptive Streams

This is a python based project that allows you to restream IPTV content to your own channels with adaptive streaming support. The project is hosted on Github and can be used for various purposes such as creating your own IPTV network or streaming media from your own server.

### Installation
To use the IPTV Restreamer with Adaptive Streams, you will need to have Python installed on your system. You will also need to install the following dependencies:

As an AI language model, I don't have access to the playlist.m3u8 file of ilook.tv or your local system. However, you can replace the IP address in the playlist.m3u8 file with your server's IP address by following these steps:

1. Open the **`playlist.m3u8`** file in a text editor.
2. Look for the IP address in the file, which should be in the format **`http://<ip_address>:<port>/stream.m3u8`**.
3. Replace the **`<ip_address>`** with your server's IP address and **`<port>`** with the port number on which you are streaming the content. For example, if you are streaming on port 8000 and your server's IP address is 192.168.1.100, the URL should be **`http://192.168.1.100:8000/stream.m3u8`**.
4. Save the file.
Once you have updated the **`playlist.m3u8`** file, you can use it as the input URL in the IPTV Restreamer with Adaptive Streams project.

```bash
git clone https://github.com/Romaxa55/iptv-restreamer.git
```

You can install the dependencies using pip, by running the following command in the terminal:

```bash
pip install -r requirements.txt
```
Alternatively, you can also use Docker to run the project.

### Usage

To use the IPTV Restreamer with Adaptive Streams, you will need to provide the following information:

- **Input URL**: The URL of the IPTV stream that you want to restream.
- **Output URL**: The URL of your own channel where you want to stream the content.
- **Adaptive Bitrate**: The bitrate at which the video will be encoded for adaptive streaming.
Once you have provided this information, you can run the project using the following command:

```bash
python main.py
```
If you are running the project using Docker, you can use the following command instead:

```
docker run -it --rm -p 8000:8000 romaxa55/iptv-restreamer
```

### Contributing

If you would like to contribute to the IPTV Restreamer with Adaptive Streams project, you can do so by submitting a pull request on Github. Before submitting a pull request, please make sure that your code follows the coding guidelines and has been tested thoroughly.

### License

The IPTV Restreamer with Adaptive Streams project is licensed under the MIT License. You can find the full license text in the LICENSE file.

### Contact
If you have any questions or need further assistance with the IPTV Restreamer with Adaptive Streams project, you can contact me on Telegram at @romaxa55. I will be happy to assist you with any issues you may encounter while using the project.

