
//var command_handlers_registry = require('./handlers.js');

register = require('./handlers.js').register;
console.log(register)

registry = register('command_handlers');
console.log(registry);
