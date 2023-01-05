from kafka import KafkaConsumer
import json
import sys
import time
import logging


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    consumer = KafkaConsumer("kube_kafka_topic",
                             bootstrap_servers=['kafka-service:9092'],
                             api_version=(0, 10, 1),
                             auto_offset_reset='latest',
                             )
    for msg in consumer:
        if msg is None or msg == '':
            logging.error("No messages received from Kafka!")
        else:
            logging.info(" current message is = {}".format(json.loads(msg.value)))
            json_output_1 = json.loads(msg.value)
            current_output = json_output_1['table'][0]
            break

    json_output_2 = json.loads(sys.argv[1])['payload']
    previous_output = json.loads(json_output_2)['table'][0]
    logging.info(f" previous message is = {previous_output}")
    
    gcs_output = {
        "Date": str(current_output["time"])[5:].replace(' ', '_'),
        "Time": current_output["$time"],
        "Strategy": current_output["strategy"],
        "Open": current_output["open"],
        "Title": current_output["title"],
        "Timeframe": current_output["timeframe"]
    }

    if current_output['$time'] == previous_output['$time']:
        logging.error('\n There is an error in Kafka pipeline: 1st and 2nd outputs are identical')
    else:
        with open("output.json", "w") as outfile:
            json.dump(gcs_output, outfile)
