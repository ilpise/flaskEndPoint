# syntax=docker/dockerfile:1
FROM arm32v7/python:3.7-buster
ADD . /flaskEndPoint
WORKDIR /flaskEndPoint
#RUN whoami
#RUN apt-get update
#RUN apt-get -y install gcc curl musl-dev libssl-dev libffi-dev
#RUN curl https://sh.rustup.rs -sSf | sh
RUN pip3 install .
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
