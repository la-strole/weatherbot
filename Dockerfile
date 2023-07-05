FROM python:slim-bullseye
# Copy files and virtual environments (be sure to include .env file with tokens)
COPY . /home
RUN apt update
# install make
RUN apt install make
# install curl
RUN apt install curl -y
WORKDIR /home
# install environment
RUN make install
