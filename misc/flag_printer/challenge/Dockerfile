FROM ubuntu:22.04

RUN /usr/sbin/useradd -u 1000 user

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
      ca-certificates socat python3\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/user/
COPY chal.py /home/user/

RUN chown root:root chal.py
RUN chmod 444 chal.py
RUN chown user:user /home/user
RUN chmod 755 /home/user

# RUN chmod a+x /home/user/chal.py

EXPOSE 1331

USER user

CMD   socat \
      TCP-LISTEN:1331,reuseaddr,fork \
      EXEC:"timeout 120 python3 /home/user/chal.py"
