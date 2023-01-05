#!/bin/bash

previous_output=$(kafkacat -C -b kafka-service:9092 -t kube_kafka_topic -o-1 -J -c1 -e)

python3 kafka_consumer.py "$previous_output"

strategy=$(jq '.Strategy' output.json)
label=$(jq '.Title' output.json)
timeframe=$(jq '.Timeframe' output.json)
EXECUTION_TIMESTAMP=$(jq '.Date' output.json)

project_name=

gsutil cp output.json gs://"$project_name"/"$label"_"$timeframe"/$strategy/$EXECUTION_TIMESTAMP

exit 0
