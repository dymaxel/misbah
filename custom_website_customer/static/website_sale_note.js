odoo.define('custom_website_customer.internal_notes', function (require) {
'use strict';
    var session = require('web.session');
    var ajax = require('web.ajax');
    var rpc = require('web.rpc');
    
    $("#internal_notes").mouseleave(function(){
        var internal_notes = $('#internal_notes').val();
        ajax.jsonRpc('/shop/payment/add_note', 'call',
            {'internal_notes': internal_notes}).then(function(output) {
      });
    });
});
