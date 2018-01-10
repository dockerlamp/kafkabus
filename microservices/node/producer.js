var kafka = require('kafka-node');

// test env settings
var producer_min_no = Math.pow(10,3);
    producer_max_no = 2*Math.pow(10,3); 
    MSG_MIN_NO = Math.pow(10,6);
    MSG_MAX_NO = 2*Math.pow(10,6);
    
    PRODUCER_ID = Math.floor(Math.random() * (producer_max_no - producer_min_no) + producer_min_no);
    DELAY = 1000

// # kafka settings
var TOPIC_NAME = 'example_topic';
    BOOTSTRAP_SERVERS = process.env.BOOTSTRAP_SERVERS
    KAFKA_CONFIG =  {
      //fetchMaxWaitMs: 1000,
      //fetchMaxBytes: 1024 * 1024 
  };


var rets = MSG_MIN_NO;
    const client = new kafka.KafkaClient({kafkaHost: BOOTSTRAP_SERVERS});
    channel = new kafka.Producer(client);
    


channel.on('ready', function () {
  setInterval(send, DELAY);
});

channel.on('error', function (err) {
  console.log('error', err);
});

function send () {
  var msg = JSON.stringify({producer_id: PRODUCER_ID,
                            msg_no: rets, 
                            topic_name: TOPIC_NAME})
  channel.send([
    {topic: TOPIC_NAME, messages: [msg]}
  ], function (err, data) {
    if (err) console.log(err);
    else console.log('sent', msg);
    ++rets
    if (rets === MSG_MAX_NO) process.exit();
  });
}
