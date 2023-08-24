odoo.define('my_module.my_script', function (require) {
    "use strict";

    var bus = require('bus.bus').bus;

    bus.on('my_channel', this, function (message) {
        if (message.type === 'my_event') {
            alert(message.message);
        }
    });
});