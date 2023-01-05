#!/bin/bash

target=$(date '+%d-%b-%Y %H:%M:59')  # 
echo "$target"

target_epoch=`date -d "$target" +"%s"`
echo "$target_epoch"

current_epoch=$(date +%s)
echo "$current_epoch"

sleep_seconds=$(( $target_epoch - $current_epoch ))

sleep $sleep_seconds".700"

# The script starts approximately at > 59.700 seconds (e.g. 14:29:59.700) every 30 minutes

node kafka_producer.js \
BINANCE \  # set market
BTCUSDT \  # set a trading pair
30 \  # set a timestamp
CM_Ultimate_MA_MTF_V2 \  # set a name of a tradingview strategy
1SMA_2EMA_3WMA_4HullMA_5VWMA_6RMA_7TEMA_8Tilson_T3=7  # set a parameter of a tradingview strategy you want to configure

exit 0
