odoo.define('odoo_website_daily_deals.daily_deals_slider', function (require) {
'use strict';
    $(document).ready(function(){
        var hasSlider = $(".four_shows_one_move").length;
        if(hasSlider != 0){
            $('.four_shows_one_move').carousel({
                interval: 5000
            });
            $(".four_shows_one_move").each(function(){
                $(this).find(".carousel-item").first().addClass("active");
            })
            $('.four_shows_one_move .carousel-item').each(function(){
              var next = $(this).next();
              if (!next.length) {
                next = $(this).siblings(':first');
              }
              next.children(':first-child').clone().appendTo($(this));

              for (var i=1;i<3;i++) {
                next=next.next();
                if (!next.length) {
                    next = $(this).siblings(':first');
                }
                next.children(':first-child').clone().appendTo($(this));
              }
            });
        }
    })
})