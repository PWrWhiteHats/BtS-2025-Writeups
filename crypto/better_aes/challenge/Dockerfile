FROM python

RUN apt update && apt install -y socat

WORKDIR /chall

COPY ./flag /chall/flag
COPY ./better_aes.py /chall/better_aes.py

EXPOSE 13377
CMD socat tcp-listen:13377,reuseaddr,fork exec:'python better_aes.py'
