$(document).ready(function () {
    // console.log(parseInt("13135345").toLocaleString())

    $(".canvas .panel").hide();
    // $(".switch#air").addClass("anchor");
    $(".switch#air").prop("checked", true);
    $(".canvas .air").show();
    // $(".switch.latest").addClass("anchor");
    $(".switch.current").prop("checked", true);
    $(".canvas .current").show();

    // mark required items
    $("input:required").prev().addClass('mark');

    //Reset button
    $("input[name=hearingReset]").click(function () {
        $(".switch#air").trigger("click");
        $(".switch.latest").trigger("click");
        // console.log('asdf')
    });


    // switch canvas
    $("input.switch").click(function () {
        var tabid = this.id;
        var tabname = this.name;
        // console.log(tabname);
        // console.log(tabid);
        $(".canvas." + tabname + " .panel").hide();
        $(".canvas." + tabname + " ." + tabid).show();
        // }
        // $("input.switch[name=" + tabname + "]").removeClass("anchor");
        // $("#" + tabid).addClass("anchor");
    });






});
