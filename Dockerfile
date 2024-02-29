FROM python:3.12.2-alpine3.19

LABEL maintainer="me@pgarcia.dev"

COPY requirements.txt /mnt/unattached_volumes/requirements.txt

COPY unattached_volumes/unattached_volumes.py /usr/local/bin/unattached_volumes

WORKDIR /mnt/unattached_volumes

RUN pip install --no-cache-dir -r /mnt/unattached_volumes/requirements.txt

ENTRYPOINT ["/usr/local/bin/unattached_volumes"]

CMD ["-h"]
