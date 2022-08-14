$(document).ready(function(){
'use strict';

            $('.js_close_popup').click(function() {
            var src = $('iframe').attr('src');
            $('iframe').attr('src', "")
            console.log(src);
                });


})