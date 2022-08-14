
odoo.define('ecommerce_store.current_stock', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.portalDetails =  publicWidget.Widget.extend({
    selector: '.oe_website_sale',
    events: {
        'change #select_customer': 'onChangeCustomer',
        'keyup #select_customer': 'getcustomers',
        'click #select_customer': 'toggle_dropdown',
        'click .list_values': 'select_customer'
    },
    start: function () {
        var def = this._super.apply(this, arguments);
        this.getcustomers();
        return def;
    },
    select_customer:function(ev){

        var id = ev.currentTarget.getAttribute('data-id');
        var name = ev.currentTarget.getAttribute('data-name');
        this.toggle_dropdown();
        $('#select_customer').attr('data-id',id);
        $('#select_customer').val(name).trigger('change');

    },
    toggle_dropdown:function(ev){
        document.getElementById("select_customers").classList.toggle("show");
    },
    getcustomers: function (ev) {
		var self= this;

        var search_string = $('#select_customer').val();

        if(search_string){
            $("#select_customers").css("display", "block");
        }
        else if(search_string==''){
            $("#select_customers").css("display", "none");
        }
        var options ="";
        this._rpc({
            route: "/getcustomers",
            params: {
                search: search_string,
            },
        }).then(function(data) {
            console.log('dataaaaaaaaaa',data);

            for (let i = 0; i < data.length; i++) {
                options += "<a style='border-bottom:1px solid;' class='list_values' data-name='"+data[i]['name']+"' data-id="+data[i]['id']+"><span>Name: </span><span>"+data[i]['name']+"<span></br><span>Phone: </span><span>"+data[i]['mobile']+"</span></br><span>Email: </span><span>"+data[i]['email']+"<span></br><span>Address: </span><span>"+data[i]['address']+"</span></a>";
            };
            $('#select_customers').html(options);
        });
    },

    onChangeCustomer:function(ev){
        var customer_id = $('#select_customer').attr('data-id');
        console.log('customer_id: ',customer_id)
        if(!customer_id) return;
        $.blockUI();
        this._rpc({
            route: "/update_order_customer",
            params: {
                customer_id: customer_id,
            },
        }).then(function (data) {
            $.unblockUI();
            alert("Customer Updated Successfully!!!");
            $(".dropdown-content").css("display", "none");

        }).then(function(){
            $.unblockUI();

        })

    },

});

});
