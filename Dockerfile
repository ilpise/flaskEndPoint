# syntax=docker/dockerfile:1
FROM arm32v7/python:3.7-buster
ADD . /flaskEndPoint
WORKDIR /flaskEndPoint
#RUN whoami
RUN apt-get update
#RUN apt-get -y install rustc gcc musl-dev libssl-dev libffi-dev
RUN apt-get -y install pcscd swig gcc libpcsclite-dev python-dev
RUN pip3 install .
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
