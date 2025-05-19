FROM debian:stable-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    qemu-system-x86 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY . /challenge

EXPOSE 4000

CMD qemu-system-x86_64 -cdrom btsctf.iso -serial tcp:0.0.0.0:4000,server,nowait -nographic -monitor none