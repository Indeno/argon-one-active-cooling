FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y i2c-tools && \
    pip install --no-cache-dir && \
    mkdir -p /data

COPY main.py /main.py
COPY run.sh /run.sh
RUN chmod +x /run.sh

CMD [ "/run.sh" ]