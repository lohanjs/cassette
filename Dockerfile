FROM python:3
# Adding build tools to make yarn install work on Apple silicon / arm64 machines
ADD music.py /

ARG TOKEN

ENV TOKEN $TOKEN

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
RUN apt-get -y update
RUN apt-get install -y ffmpeg
CMD ["python3", "/music.py"]