FROM ubuntu:25.04@sha256:adb623490ed6f4252989513900f1e88dc11c7974577de44d6959181a354a427a

RUN apt update && apt install -y socat

WORKDIR /app
RUN useradd ctf

COPY ./hexdumper /app/hexdumper
COPY ./flag /app/flag
RUN chmod +x /app/hexdumper
RUN chmod 444 /app/flag

USER ctf

EXPOSE 1337
CMD socat tcp-l:1337,reuseaddr,fork exec:/app/hexdumper
