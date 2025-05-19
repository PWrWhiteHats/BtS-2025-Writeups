FROM ubuntu:22.04

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
      ca-certificates socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/user/
COPY flag lotto.bin /home/user/

RUN chown root:root flag lotto.bin
RUN chmod 444 flag lotto.bin
RUN chown user:user /home/user
RUN chmod 755 /home/user

RUN chmod a+x /home/user/lotto.bin

EXPOSE 1337

USER user

CMD   socat \
      TCP-LISTEN:1337,reuseaddr,fork \
      EXEC:"timeout 120 /home/user/lotto.bin"
