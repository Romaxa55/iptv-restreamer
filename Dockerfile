FROM linuxserver/ffmpeg
WORKDIR /app
COPY . .
RUN \
    echo "**** install runtime ****" && \
    apt-get update && \
    apt-get install -y \
      python3  \
      python3.10-venv \
      python3-pip  \
    && \
    echo "**** clean up ****" && \
    rm -rf \
      /var/lib/apt/lists/* \
      /var/tmp/* && \
    echo "**** install python requirements.txt ****" && \
    pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["main.py"]
CMD ["python3", "main.py"]