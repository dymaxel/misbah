odoo.define("sh_qty_shop_ajax_moq.website_sale", function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');
    var wSaleUtils = require("website_sale.utils");
    require('website_sale.website_sale');
    

    publicWidget.registry.WebsiteSale.include({
        read_events: {
            "click .sh_add_cart, .sh_add_cart_dyn": "_onClickAddDirectCart",
            'change input[name="add_qty"]': '_onChangeAddQuantity',
        },
        _onClickAddDirectCart: function (ev) {
            this._addNewProducts($(ev.currentTarget));
        },

        /**
         * @private
         */

        _addNewProducts: function ($el) {
            console.log("add product");
            var self = this;
            var productID = $el.data("product-product-id");
            if ($el.hasClass("sh_add_cart_dyn")) {
                productID = $el.parent().find(".product_id").val();
                if (!productID) {
                    // case List View Variants
                    productID = $el.parent().find("input:checked").first().val();
                }
                productID = parseInt(productID, 10);
            }

            var $form = $el.closest("form");
            var templateId = $form.find(".product_template_id").val();
            // when adding from /shop instead of the product page, need another selector
            if (!templateId) {
                templateId = $el.data("product-template-id");
            }
            var productReady = this.selectOrCreateProduct($el.closest("form"), productID, templateId, false);

            var line_id = parseInt($el.data("line-id"), 10);

            productReady.then(function (productId) {
                productId = parseInt(productId, 10);

                if (productId) {
                    console.log($el.closest("form")['0']['1']['dataset']['min']);
                    var iniqty = $el.closest("form")[0][1]['dataset']['min'];
                    // // console.log($el.closest("form").find(".quantity").val() || 1.0);
                    // console.log($el.closest("form").find("setqty").val());
                    return self
                        ._rpc({
                            route: "/shop/cart/update_json",
                            params: {
                                product_id: productId,
                                line_id: line_id,
                                add_qty: $el.closest("form").find(".quantity").val() || 1.0,
                            },
                        })

                        .then(function (data) {
                            var $q = $(".my_cart_quantity");
                            if (data.cart_quantity) {
                                $q.parents("li:first").removeClass("d-none");
                                $(".o_wsale_my_cart").show();
                                $(".my_cart_quantity").text(data.cart_quantity);
                            }
                            wSaleUtils.animateClone($(".o_wsale_my_cart"), $el.closest("form"), 20, 10);
                        });
                }
            });
        },
    
        _onClickAddCartJSON: function (ev) {
            ev.preventDefault();
            console.log("_onClickAddCartJSON");
            var $link = $(ev.currentTarget);

            var $input = $link.closest(".input-group").find("input");
            var min = parseFloat($input.data("min") || 0);
            var setqty = parseFloat($input.data("setqty") || 1);
            var max = parseFloat($input.data("max") || Infinity);
            var quantity = ($link.has(".fa-minus").length ? -setqty : setqty) + parseFloat($input.val() || 0, 10);
            var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
            $input.val(newQty).trigger("change");
            return false;
        },
        _onChangeAddQuantity: function (ev) {
            console.log("_onChangeAddQuantity");
            ev.preventDefault();
            var $link = $(ev.currentTarget);
            var data = $link.closest('input[name="add_qty"]').val();
            var default_value = $link.closest('input[name="add_qty"]').data("setqty");
            if (parseInt(data) < parseInt(default_value)) {
                var set_data = default_value;
                $link.closest('input[name="add_qty"]').val(set_data);
            } else if (parseInt(data) > parseInt(default_value)) {
                var divided_value = Math.ceil(parseInt(data) / parseInt(default_value));
                var set_data = divided_value * parseInt(default_value);
                $link.closest('input[name="add_qty"]').val(set_data);
            }
            this._super.apply(this, arguments);
            return false;
        },

        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
            console.log("_changeCartQuantity");
            this._super.apply(this, arguments);
            var data = value;
            var default_value = $input.data("setqty");
            if (value != 0) {
                if (parseInt(data) < parseInt(default_value)) {
                    var set_data = default_value;
                    $input.val(set_data);
                } else if (parseInt(data) > parseInt(default_value)) {
                    var divided_value = Math.ceil(parseInt(data) / parseInt(default_value));
                    var set_data = divided_value * parseInt(default_value);
                    $input.val(set_data);
                }
            }
        },
    });
});
