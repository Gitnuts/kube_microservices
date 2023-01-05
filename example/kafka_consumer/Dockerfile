FROM python:3.9

RUN apt-get update && \
    apt-get install -y kafkacat jq

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

#  To use GCP, you need credentials for a project

COPY gcp_credentials.json /usr/src/app/gcp_credentials.json
COPY kafka_consumer.py /usr/src/app/kafka_consumer.py
COPY exec.sh /usr/src/app/exec.sh


RUN chmod +x /usr/src/app/exec.sh
WORKDIR /usr/src/app/

ENTRYPOINT ["/usr/src/app/exec.sh"]
