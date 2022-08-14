$(document).ready(function(){
    $(document).on('change','#web_img',function(){
    var text = document.getElementById("img_size");
    var style = document.getElementsByClassName("style");
        if (this.checked && style != 'style_4'){
            text.style.display = "block";
        }
        else {
            text.style.display = "none";
        }
    });


})