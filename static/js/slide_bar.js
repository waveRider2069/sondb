$(document).ready(function () {

    $("form#personalForm,form#hearingForm").find(".range input[type=range]").each(function () {
        var curvalue = $(this).val();
        var max = $(this).attr("max");
        var min = $(this).attr("min");
        if (curvalue == min) {
            $(this).siblings(".slide_handle").text("").css({"background": "#ccc", "border-color": "#ccc"});
        } else {
            $(this).siblings(".slide_handle").text(curvalue).css({
                "background": "#199ED8",
                "border-color": "#199ED8"
            });
        }
        var barwidth = 152;
        var handlewidth = $(this).siblings(".slide_handle").outerWidth();
        var full_percent = (barwidth - handlewidth + 1) / barwidth * 100;
        var width = (full_percent / (max - min) * (curvalue - min)) + "%";
        // console.log(width)
        var size = width + " 100%";
        $(this).siblings(".slide_prog").css({"background-size": size});
        $(this).siblings(".slide_handle").css({"left": width});
    });


    var $elem = $(".range input[type=range]");
    $elem.on("input", function () {
        var curvalue = $(this).val();
        var max = $(this).attr("max");
        var min = $(this).attr("min");
        if (curvalue == min) {
            $(this).siblings(".slide_handle").text("").css({"background": "#ccc", "border-color": "#ccc"});
        } else {
            $(this).siblings(".slide_handle").text(curvalue).css({"background": "#199ED8", "border-color": "#199ED8"});
        }
        var barwidth = $(this).outerWidth();
        var handlewidth = $(this).siblings(".slide_handle").outerWidth();
        var full_percent = (barwidth - handlewidth + 1) / barwidth * 100;
        var width = (full_percent / (max - min) * (curvalue - min)) + "%";
        // console.log(width)
        var size = width + " 100%";
        $(this).siblings(".slide_prog").css({"background-size": size});
        $(this).siblings(".slide_handle").css({"left": width});
    });

    $("form#personalForm,form#hearingForm").on("reset", function () {
        $(this).find(".range input[type=range]").each(function () {
            var curvalue = $(this).val();
            var max = $(this).attr("max");
            var min = $(this).attr("min");
            if (curvalue == min) {
                $(this).siblings(".slide_handle").text("").css({"background": "#ccc", "border-color": "#ccc"});
            } else {
                $(this).siblings(".slide_handle").text(curvalue).css({
                    "background": "#199ED8",
                    "border-color": "#199ED8"
                });
            }
            var barwidth = 152;
            var handlewidth = $(this).siblings(".slide_handle").outerWidth();
            var full_percent = (barwidth - handlewidth + 1) / barwidth * 100;
            var width = (full_percent / (max - min) * (curvalue - min)) + "%";
            console.log(barwidth);
            console.log(handlewidth);
            console.log(full_percent);
            // console.log(width)
            var size = width + " 100%";
            $(this).siblings(".slide_prog").css({"background-size": size});
            $(this).siblings(".slide_handle").css({"left": width});
        })
    })

});