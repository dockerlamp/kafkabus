var kafka = require('kafka-node');

var bus = require("../../systembus/bus.json");
    events_cfg = require("../../systembus/events.json");

// kafka settings
var BOOTSTRAP_SERVERS = bus['bootstrap_servers']


function whenProducerReady() {
    return new Promise(function (resolve, reject) {
        var client = new kafka.KafkaClient({kafkaHost: BOOTSTRAP_SERVERS});
            producer = new kafka.Producer(client);
        producer.on('ready', function () {
            resolve(producer);
        });
    });
}


async function emit(event_name, event) {

    var producer = await whenProducerReady();
    event_cfg = events_cfg[event_name]
    payload = {topic:  event_cfg['topic'], messages: [event]};
    if (event_cfg['key']!= 'None') {payload['key'] = event_cfg['key']};

    producer.send([payload], 
        function (err, data) {
            if (err) console.log(err);
            else console.log('raised event', event);
    });
}

exports.emit = emit
