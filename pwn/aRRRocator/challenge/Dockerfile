FROM ubuntu:22.04@sha256:67cadaff1dca187079fce41360d5a7eb6f7dcd3745e53c79ad5efd8563118240

RUN apt update && apt install -y qemu-user socat binutils-riscv64-linux-gnu libc6-riscv64-cross libc6-dev-riscv64-cross libgcc-s1-riscv64-cross libstdc++6-riscv64-cross

WORKDIR /app
RUN useradd ctf

COPY ./arrrocator /app/arrrocator
RUN chmod +x /app/arrrocator
COPY ./flag /app/flag
RUN chmod 444 /app/flag

USER ctf

EXPOSE 1337

CMD socat tcp-l:1337,reuseaddr,fork exec:"qemu-riscv64 -L /usr/riscv64-linux-gnu /app/arrrocator"
