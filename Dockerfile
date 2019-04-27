FROM alpine:3.8

RUN apk add --update bash gcc musl-dev git make zlib-dev python3 python3-dev

WORKDIR /app

RUN git clone https://github.com/lh3/bwa.git

WORKDIR /app/bwa

RUN make

ADD requirements.txt /app/requirements.txt
RUN pip3 install --upgrade --force-reinstall -r /app/requirements.txt

ADD bwa_aligner /app/bwa_aligner
ADD run.py /app/run.py

RUN chmod +x /app/run.py

CMD ["python3", "-u", "/app/run.py"]