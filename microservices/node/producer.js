var kafka = require('kafka-node');

var bus = require("../../systembus/bus.json");
    commands_cfg = require("../../systembus/commands.json");


// test env settings
var command_names = Object.keys(commands_cfg)
    COMMAND_NAME = command_names[Math.floor(Math.random()*command_names.length)];
    COMMAND_CFG = commands_cfg[COMMAND_NAME]
    OBJ_ID = Math.floor(Math.random() * (9*Math.pow(10,4) - 8*Math.pow(10,4)) + 8*Math.pow(10,4));
    PRODUCER_ID = Math.floor(Math.random() * (2*Math.pow(10,3) - Math.pow(10,3)) + Math.pow(10,3));
    MSG_NO_RANGE = [Math.pow(10,6), 2*Math.pow(10,6)]
    DELAY = 2000


// kafka settings
var BOOTSTRAP_SERVERS = bus['bootstrap_servers']
    TOPIC_NAME = COMMAND_CFG['topic']
    KEY = (COMMAND_CFG['key'] == "None") ? "None" : COMMAND_CFG['key']+'.'+OBJ_ID


console.log(COMMAND_NAME, OBJ_ID, PRODUCER_ID, MSG_NO_RANGE)
console.log(BOOTSTRAP_SERVERS, TOPIC_NAME, KEY)

var client = new kafka.KafkaClient({kafkaHost: BOOTSTRAP_SERVERS});
    producer = new kafka.Producer(client);
    msg_no = MSG_NO_RANGE[0];


    producer.on('ready', function () {
    setInterval(send, DELAY);
    });
    
    producer.on('error', function (err) {
    console.log('error', err);
    });

function send () {
    var msg = JSON.stringify({
        'uuid' : Math.floor(Math.random() * (6*Math.pow(10,5) - 5*Math.pow(10,5)) + 5*Math.pow(10,5)),
        'source' : PRODUCER_ID,
        'msg' : msg_no,
        'command_name' : COMMAND_NAME,
    })
    producer.send([
        {topic: TOPIC_NAME, messages: [msg]}
    ], function (err, data) {
        if (err) console.log(err);
        else console.log('sent', msg);
        ++msg_no
        if (msg_no === MSG_NO_RANGE[1]) process.exit();
    });
    }
