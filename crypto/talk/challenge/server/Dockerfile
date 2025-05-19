# tcpdump -i eth0 port 8443 -w /app/traffic.pcap -A &
FROM python:3.11-slim

RUN apt-get update && apt-get install -y tcpdump iproute2
RUN pip install cryptography

WORKDIR /app
COPY server.py .
COPY crypto.py .

EXPOSE 8443
CMD ["python", "server.py"]