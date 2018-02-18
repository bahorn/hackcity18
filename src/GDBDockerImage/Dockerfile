FROM alpine:3.5
RUN apk add --no-cache wget
# Stolen from: https://github.com/frol/docker-alpine-python3/blob/master/Dockerfile
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
RUN pip3 install requests
COPY ./local/gdbserver /tools/
COPY ./local/announce_death.py /tools/
ADD init.sh /
RUN chmod +x /init.sh
RUN mkdir /target/
RUN mkdir /setup/
RUN mkdir /trigger/
EXPOSE 1234
ENTRYPOINT ["/init.sh"]
