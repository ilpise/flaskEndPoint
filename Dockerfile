# syntax=docker/dockerfile:1
FROM python:3.7-buster
ADD . /flaskEndPoint
WORKDIR /flaskEndPoint
RUN pip3 install .
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
