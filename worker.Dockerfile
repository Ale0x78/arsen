FROM node:lts-buster-slim

COPY vv8.deb /tmp/vv8.deb



RUN apt update
RUN apt install -y gcc git curl make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev 


RUN git clone https://github.com/pyenv/pyenv /.pyenv

ENV PYENV_ROOT /.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN pyenv install 3.11.2
RUN pyenv global 3.11.2
RUN pyenv rehash

RUN apt install -y /tmp/vv8.deb
COPY app /app
RUN pip3 install -r /app/req.txt

WORKDIR /app/crawler

RUN npm install

WORKDIR /app

ENTRYPOINT /.pyenv/shims/celery -A worker worker --loglevel=info