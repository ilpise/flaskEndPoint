# syntax=docker/dockerfile:1
FROM arm32v7/python:3.7-buster
ADD . /flaskEndPoint

RUN apt-get update
# Add packages
RUN apt-get -y install pcscd swig gcc rustc libpcsclite-dev python3.7-dev

# Debug packages
RUN apt-get -y install minicom pcsc-tools

# Change to flask app directory and run install
WORKDIR /flaskEndPoint
RUN pip3 install .

# Change rights to entrypoint bash script and run it
RUN ["chmod", "+x", "/flaskEndPoint/entrypoint.sh"]
ENTRYPOINT ["./entrypoint.sh"]
