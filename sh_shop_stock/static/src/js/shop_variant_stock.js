odoo.define("sh_shop_stock.website_sale", function (require) {
    "use strict";

    var ajax = require("web.ajax");

    function product_variant() {
        var ret = ajax
            .jsonRpc("/product/shop_product_var_stock", "call", {
                product_id: $(".product_id").val(),
            })
            .then(function (data) {
                if (data >= 0) {
                    if (data > 0) {
                        $("#variant_stock").html('<span class="alert alert-success"><strong>In Stock (' + data + " Quantity Left)</strong></span>");
                    } else {
                        $("#variant_stock").html('<span class="alert alert-danger"><strong>Out Of Stock</strong></span>');
                        $("#add_to_cart").hide();
                        $(".css_quantity input-group oe_website_spinner").hide();
                    }
                } else {
                    if (data == -2) {
                        $("#variant_stock").html('<span class="alert alert-success"><strong>In Stock</strong></span>');
                    } else {
                        $("#variant_stock").hide();
                    }
                }
            });
    }

    $(document).ready(function () {
        "use strict";
        product_variant();

        $(".oe_website_sale").each(function () {
            var oe_website_sale = this;

            $(oe_website_sale).on("change", "input.js_variant_change, select.js_variant_change", function (ev) {
                product_variant();
            });
        });
    });
});
