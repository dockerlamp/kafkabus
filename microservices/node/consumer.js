var kafka = require('kafka-node');

// test env settings
var consumer_min_no = 3*Math.pow(10,3);
    consumer_max_no = 4*Math.pow(10,3); 
    CONSUMER_ID = Math.floor(Math.random() * (consumer_max_no - consumer_min_no) + consumer_min_no);

// # kafka settings
var BOOTSTRAP_SERVERS = process.env.BOOTSTRAP_SERVERS
    TOPIC_NAME = 'example_topic';

    KAFKA_CONFIG = {
        kafkaHost: BOOTSTRAP_SERVERS,
        groupId: 'example_group', // use groups for durable queue
        autoCommit: true, // for groups mode
        fromOffset: 'earliest', // default latest
    };


var topics = [{ topic: TOPIC_NAME }];
    const client = new kafka.KafkaClient({kafkaHost: BOOTSTRAP_SERVERS});
    //var consumer = new kafka.Consumer(client, topics, KAFKA_CONFIG);
    var consumer = new kafka.ConsumerGroup(KAFKA_CONFIG, TOPIC_NAME);

consumer.on('message', function (message) {
    var value = JSON.parse(message['value'])
    value['consumer_id'] = CONSUMER_ID;
    value['partition'] = message['partition'];
    value['offset'] = message['offset'];

    console.log('received', JSON.stringify(value));
});

consumer.on('error', function (err) {
  console.log('error', err);
});

