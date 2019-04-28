$(document).ready(function() {
    $(".slider").each(function() {
        var cur = $(this);
        var min = -20;
        var max = 125;
        cur.slider({
            orientation: "vertical",
            min: min,
            max: max,
            step: 5,
            values: [min, max],
            range: true,
            // create: function() {handle.text( $( this ).slider( "value" ) );},
            slide: function(event, ui) {
                // console.log(ui);
                if ((ui.handleIndex == 1 && ui.value == max) || (ui.handleIndex == 0 && ui.value == min)) {
                    $(ui.handle).text("");
                    $(ui.handle).css({ "background-color": "#ccc" });
                } else {
                    $(ui.handle).text(ui.value);
                    $(ui.handle).css({ "background-color": "#199ED8" })
                }
            }
        });
    })
    // var handle = $( "#custom-handle" );


    $(".sliderAgeRange").slider({
        min: 0,
        max: 100,
        step: 5,
        values: [0, 100],
        range: true,
        // create: function() {handle.text( $( this ).slider( "value" ) );},
        slide: function(event, ui) {
            // console.log(ui);
            if ((ui.handleIndex == 1 && ui.value == 100) || (ui.handleIndex == 0 && ui.value == 0)) {
                $(ui.handle).text("");
                $(ui.handle).css({ "background-color": "#ccc" });
            } else {
                $(ui.handle).text(ui.value);
                $(ui.handle).css({ "background-color": "#199ED8" });
            }
        }
    });



    $(".sliderAge").slider({
        min: 0,
        max: 100,
        step: 1,
        value: 0,
        range: false,
        create: function(event, ui) {$(ui.handle).text(ui.value); },
        slide: function(event, ui) {
            // console.log(ui);
            $(ui.handle).text(ui.value);
            if (ui.value == 100 || ui.value == 0) {
                // $(ui.handle).text("");
                $(ui.handle).css({ "background-color": "#ccc" });
            } else {
                // $(ui.handle).text(ui.value);
                $(ui.handle).css({ "background-color": "#199ED8" });
            }
        }
    });


});