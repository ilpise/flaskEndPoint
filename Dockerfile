FROM arm32v7/python:3.7-buster
ADD . /flaskEndPoint
WORKDIR /flaskEndPoint
RUN pip3 install .
RUN ["chmod", "+x", "/flaskEndPoint/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
