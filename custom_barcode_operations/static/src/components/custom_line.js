
/** @odoo-module **/

import LineComponent from '@stock_barcode/components/line';

import { patch } from 'web.utils';
var session = require('web.session');
var rpc = require('web.rpc');
patch(LineComponent.prototype, 'custom_barcode_operations', {
    addNotes(ev) {
        this.env.model.updateLineNotes(this.line.virtual_id,event.target.value);
    },

    addQuantity(quantity, ev) {
        var l_comp = this;

        //show popup
        $('#BarCode').modal('show');


        $('.close_custom_popup').click(function(){
            $('#barcode_pass').val('');
             $("#validation_text").html('');
             /*location.reload();*/
             l_comp = '';

        })

        //check entered password in db

        $(".barcd_pass").click(function () {
            var self = this;
            var barcode_pass = $('#barcode_pass').val();
            var current_user_id = session.uid
            rpc.query({
                model: 'res.users',
                method: 'get_barcode_password',
                args: [{
                    'user_id': current_user_id,
                    'barcode_pass':barcode_pass,

                }]
            }).then(function (data){
                if(data){
                    if(l_comp && l_comp.line.qty_done === 0){
                        l_comp.env.model.updateLineQty(l_comp.line.virtual_id, quantity);
                    }
                    $('#BarCode').modal('hide');
                    $('#barcode_pass').val('');
                }
                else if(!data){
                    $("#validation_text").html("Please Enter Correct Password");
                    $('#barcode_pass').val('');
                }
            });
        });
    },
});
