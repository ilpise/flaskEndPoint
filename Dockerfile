FROM python:3.7.10
ADD . /flaskEndPoint
WORKDIR /flaskEndPoint
RUN pip install .
ENTRYPOINT [ "python" ]
CMD [ "run.py" ]
