FROM linuxserver/ffmpeg
WORKDIR /app
RUN \
    echo "**** install runtime ****" && \
    apt-get update && \
    apt-get install -y \
      python3  \
      python3-pip  \
    && \
    echo "**** clean up ****" && \
    rm -rf \
      /var/lib/apt/lists/* \
      /var/tmp/* && \
    useradd -ms /bin/bash myuser && \
    chown -R myuser:myuser .
USER myuser
COPY . .
RUN python3 -m venv /opt/venv &&  \
    echo "**** install python requirements.txt ****" && \
    pip3 install -r requirements.txt

EXPOSE 8000/tcp
CMD ["main.py"]
ENTRYPOINT ["/usr/bin/python3"]