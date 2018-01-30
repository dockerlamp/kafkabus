

function register(directory) {

    var registry = {}
    require("fs").readdirSync(directory).forEach(function(file) {
        handler = require('./'+directory + '/' + file);
        Object.assign(registry, handler);
    });
    return registry
}

exports.register = register