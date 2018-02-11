var commands_cfg = require("../../../systembus/commands.json");
    events_cfg = require("../../../systembus/events.json");
    handlers_cfg = require("../../../systembus/handlers.json");

    emit = require('../event_producer.js').emit;


function createContainerCommandHandler(command) {
    console.log('handling command', JSON.stringify(command));
    // TODO do stuff here...

    var command_name = command['command_name']
        handler_name = commands_cfg[command_name]['handler']

    handlers_cfg[handler_name]['event_names'].forEach(function(event_name){
        event = {
            'event_name' : event_name,
            'uuid' : command['uuid'],
            'source' : command['source'],
            }
        emit(event_name, event)
    });
}

module.exports = {createContainerCommandHandler}