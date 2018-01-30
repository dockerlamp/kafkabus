var commands_cfg = require("../../../systembus/commands.json");
    events_cfg = require("../../../systembus/events.json");
    handlers_cfg = require("../../../systembus/handlers.json");


function createContainer(command) {
    console.log('handling command', command);
    // TODO do stuff here...

    var command_name = command['command_name']
        handler_name = commands_cfg[command_name]['handler']

    handlers_cfg[handler_name]['event_names'].forEach(function(event_name){
        console.log(event_name);
    });
}

module.exports = {createContainer}