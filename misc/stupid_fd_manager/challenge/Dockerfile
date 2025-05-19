FROM ubuntu:latest

RUN apt update && apt install -y socat

WORKDIR /app
RUN useradd ctf

COPY ./fd_manager /app/fd_manager
COPY ./flag /app/flag
RUN chmod +x /app/fd_manager
RUN chmod 444 /app/flag

USER ctf

EXPOSE 1337
CMD socat tcp-l:1337,reuseaddr,fork exec:/app/fd_manager
