$(document).ready(function() {

    var sliderA = $(".upperma");
    var sliderB = $(".uppermb");

    var bar_topA = $("#bar250a").offset().top;
    var bar_topB = $("#bar250b").offset().top;

    var bar_innerheigt = $("#bar250a").innerHeight();
    var slider_line_width = parseInt($("#up250a").css("borderWidth"), 10);

    var press = false;
    $(document).mouseup(function() {
        press = false;
    });

    sliderA.mousedown(function() {
        press = true;
    });
    sliderA.mousemove(function(event) {
        if (press) {
            var cur = event.pageY - bar_topA + 2;
            // console.log(cur);
            if (cur >= bar_innerheigt) {
                $(this).css({ "bottom": "1px" });
            } else if (cur < 1) {
                $(this).css({ "top": "-1px" });
            } else {
                $(this).css({ "top": cur * slider_line_width - 3 + "px" });
            }
        }
    });

    sliderB.mousedown(function() {
        press = true;
    });
    
    sliderB.mousemove(function(event) {
        if (press) {
            var cur = event.pageY - bar_topB + 2;
            // console.log(cur);
            if (cur >= bar_innerheigt) {
                $(this).css({ "bottom": "1px" });
            } else if (cur < 1) {
                $(this).css({ "top": "-1px" });
            } else {
                $(this).css({ "top": cur * slider_line_width - 3 + "px" });
            }
        }
    });



});