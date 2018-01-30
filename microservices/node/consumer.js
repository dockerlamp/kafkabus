var kafka = require('kafka-node');

var bus = require("../../systembus/bus.json");
    commands_cfg = require("../../systembus/commands.json");

    register = require('./handlers.js').register;
    command_handlers_registry = register('command_handlers');


// kafa consumer specific settings
var TOPIC_NAME = bus['channels']['container_commands']['topic']
    BOOTSTRAP_SERVERS = bus['bootstrap_servers']
    AUTO_OFFSET_RESET = bus['channels']['container_commands']['auto_offset_reset']
    GROUP_ID = bus['channels']['container_commands']['group_id']
    KAFKA_CONFIG = {
        kafkaHost: BOOTSTRAP_SERVERS,
        groupId: GROUP_ID, // use groups for durable queue
        autoCommit: false, // for groups mode
        fromOffset: AUTO_OFFSET_RESET, // default latest
    };


function startReceivingCommands(){
    var client = new kafka.KafkaClient({kafkaHost: BOOTSTRAP_SERVERS});
        consumer = new kafka.ConsumerGroup(KAFKA_CONFIG, TOPIC_NAME);
        topics = [{ topic: TOPIC_NAME }];

        consumer.on('message', function (message) {
            var command = JSON.parse(message['value'])     
            console.log('received', JSON.stringify(command), 'key', message['key'], 'group_id', GROUP_ID, 'partition', message['partition'], 'offset', message['offset']);
    
            var command_name = command['command_name']
                handler_name = commands_cfg[command_name]['handler']
            // handle command
            handler = command_handlers_registry[handler_name]
            handler(command);
            consumer.commit(function(err, data) {});
        });     
}

startReceivingCommands()