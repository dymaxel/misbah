odoo.define('custom_barcode_operations.signature', function (require) {
    'use strict';

    var SignatureCustom = require('web.signature_dialog');
    SignatureCustom.include({
        template: "custom_barcode_operations.signature_dialog",
    });
});
