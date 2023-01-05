const { Kafka } = require('kafkajs')
const TradingView = require("/usr/src/app/@mathieuc/tradingview");

const args = process.argv.slice(2);

const market = args[0];
const stock = args[1];
const timeframe = args[2];
const strategy = args[3];

let client = new TradingView.Client();

var data = {};
data.table = [];

const kafka = new Kafka({
  brokers: ['kafka-service:9092'], 
})
const producer = kafka.producer()

const run = async () => {

  producer.connect()
  let chart = new client.Session.Chart();

  chart.setMarket( market + ":" + stock,  {
    timeframe: timeframe,
    to: Math.round(Date.now() / 1000) - 3000,// 3000 seconds from now
    range: -1,
  });

  let publicFmp = TradingView.searchIndicator(strategy)

  publicFmp.then(async (indicator) => {

    TradingView.getIndicator(indicator[0].id).then(async (indic) => {

      if (args.length > 4) {
        for (var x = 4; x < args.length; x++) {
          Object.keys(indic.inputs).forEach(key => {
            if (indic.inputs[key].inline === args[x].split('=')[0]) {
              var arg_value = args[x].split('=')[1];
              if (['float', 'integer'].includes(indic.inputs[key].type)) {
                arg_value = parseInt(arg_value)
              }
              indic.inputs[key].value = arg_value;
            }
          })
        }
      }

      const study = new chart.Study(indic);

      study.onUpdate(() => {
        var materials = study.periods[0];
        var t = new Date(study.periods[0].$time * 1000);
        var t1 = t.toUTCString();

        var str1 = `{
          "title": "`+ stock +`",
          "strategy": "`+ strategy +`",
          "time": "`+ t1 + `",
          "timeframe": "`+ timeframe + `",
          "open": "`+ chart.periods[0].open +`", 
          "close": "`+ chart.periods[0].close +`" 
        }`;

        var info = JSON.parse(str1);
        var result = {};

        Object.keys(info)
        .forEach(key => result[key] = info[key]);
        Object.keys(materials)
        .forEach(key => result[key] = materials[key]);

        data.table.push(result);
        console.log(data)
        producer.send({
        	topic: 'kube_kafka_integration',
            messages: [
            { value: JSON.stringify(data)},
            ]})

        client.end()
        

        setTimeout(() => {
          chart.fetchMore(-2);
        }, 1);
      });
  });
  });
  setTimeout(() => {producer.disconnect()}, 10000);
}
run().catch(console.error)
