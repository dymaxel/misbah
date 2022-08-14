odoo.define('ecommerce_store.update_weekdays', function (require) {
'use strict';
var session = require('web.session');

var rpc = require('web.rpc');
    $('.weekday').on('change', function() {
        var self = this;

        let checkboxes = document.querySelectorAll('input[name="weekday"]:checked');
        let values = [];
        checkboxes.forEach((checkbox) => {
            values.push(checkbox.value);
        });


        rpc.query({
          model: 'sale.order',
          method: 'update_week_days',
          args: [{
                    'values':values,
                }]
          }).then(function(output) {

          });

    });
});

