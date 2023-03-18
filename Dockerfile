FROM linuxserver/ffmpeg
WORKDIR /app
COPY . .
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
      /var/tmp/*

RUN echo "**** install python requirements.txt ****" && \
    pip3 install -r requirements.txt

EXPOSE 8000/tcp
CMD ["main.py"]
ENTRYPOINT ["/usr/bin/python3"]