FROM python:3.10-slim

# --- NETFREE CERT INSTALL ---
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh 
RUN sh /home/netfree-unix-ca.sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
# --- END NETFREE CERT INSTALL ---

RUN apt-get update && \
    apt-get install -y ca-certificates git gcc libglib2.0-0 libsm6 libxrender1 libxext6 libgl1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "yolo.py"]
CMD ["python", "conversion_to_json.py"]
