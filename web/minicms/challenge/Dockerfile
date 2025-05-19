FROM php:8.0-apache

WORKDIR /var/www/html

RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY users.json /var/www/html/users.json
COPY index.php /var/www/html/index.php
COPY flag /root/flag.txt
COPY *.php /var/www/html/
COPY *.html /var/www/html/

RUN chown root:root /root/flag.txt && chmod 600 /root/flag.txt

RUN useradd -m minicms && \
    chown minicms:minicms /home/minicms

COPY uptime.c /tmp/uptime.c
RUN gcc -o /home/minicms/file_JeqsmJ6xwH.bin /tmp/uptime.c && \
    rm -f /tmp/uptime.c

RUN chown root:root /home/minicms/file_JeqsmJ6xwH.bin && \
    chmod u+s /home/minicms/file_JeqsmJ6xwH.bin

RUN echo "DocumentRoot /var/www/html" >> /etc/apache2/sites-available/000-default.conf

RUN cd /home/minicms && \
    echo "#!/bin/bash" > /home/minicms/entrypoint.sh && \
    echo "cd /home/minicms" > /home/minicms/testscript.sh && \
    for i in $(seq 1 100); do \
        head -c $((RANDOM % 1000 + 100)) /dev/urandom > "file_$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 10).bin"; \
    done

EXPOSE 8000

USER minicms

ENTRYPOINT ["php", "-S", "0.0.0.0:8000", "-t", "/var/www/html"]
