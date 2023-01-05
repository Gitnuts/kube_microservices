FROM node:16

# @mathieuc js package is required to extract data from TradingView
COPY @mathieuc/tradingview /usr/src/app/@mathieuc/tradingview

COPY kafka_producer.js usr/src/app/kafka_producer.js
COPY exec.sh usr/src/app/exec.sh

WORKDIR /usr/src/app/

RUN npm install kafkajs
RUN npm install
