FROM python

RUN apt update && apt install -y socat

WORKDIR /chall

COPY ./flag /chall/flag
COPY ./server_roulette.py /chall/server_roulette.py

EXPOSE 1337
CMD socat tcp-listen:1337,reuseaddr,fork exec:'python server_roulette.py'

