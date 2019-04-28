$(document).ready(function () {
    // console.log(parseInt("13135345").toLocaleString())
    $("form.unfolded").each(function () {
        $(this).css({"display": "block"});
        $(this).prev(".unfold").addClass("anchor");
    });
    // var unfold_id = $("form.unfolded").css({ "display": "block" }).prop("id");
    // $(".unfold.line[name=" + unfold_id + "]").addClass("anchor");

    // $(".canvas .panel").hide();
    // // $(".switch#air").addClass("anchor");
    // $(".switch#air").prop("checked", true);
    // $(".canvas .air").show();
    // // $(".switch.latest").addClass("anchor");
    // $(".switch.latest").prop("checked", true);
    // $(".canvas .latest").show();

    // mark required items
    $("input:required").prev().addClass('mark');

    // //Reset button
    // $("input[name=hearingReset]").click(function () {
    //     $(".switch#air").trigger("click");
    //     $(".switch.latest").trigger("click");
    //     // console.log('asdf')
    // });


    // unfold field
    $("div.unfold").click(function () {
        var it = $(this);
        var banner = it.next();
        banner.slideToggle(500, function () {
            if (banner.is(':visible')) {
                it.addClass("anchor");
                // arrow.css({ "transform": "rotateZ(180deg) translateY(-50%)", "transition": "transform 0.5s" });
            } else {
                it.removeClass("anchor");
                // arrow.css({ "transform": "rotateZ(0) translateY(50%)", "transition": "transform 0.5s" });
            }
        });
    });


    // // switch canvas
    // $("input.switch").click(function () {
    //     var tabid = this.id;
    //     var tabname = this.name;
    //     // console.log(tabname);
    //     // console.log(tabid);
    //     $(".canvas." + tabname + " .panel").hide();
    //     $(".canvas." + tabname + " ." + tabid).show();
    //     // }
    //     // $("input.switch[name=" + tabname + "]").removeClass("anchor");
    //     // $("#" + tabid).addClass("anchor");
    // });


    // checkbox to sigle choice
    $("input.single:checkbox").click(function () {
        var $it = $(this);
        var ischecked = $it.prop('checked');
        var domName = $it.attr("name");
        var domId = $it.attr("id");
        if (ischecked) {
            $("input[name=" + domName + "]").not("#" + domId).prop('checked', false);
        }
    });

    //remove project from subject
    var dismiss_proj = function () {
        var title = $(this).parent().siblings(".tag").text();
        var res = window.confirm("Sure to remove the subject form project '" + title + "'")
        if (res) {
            $proj = $(this).parent().parent();
            $proj.fadeOut(400, function () {
            });
            setTimeout('$proj.remove()', 450)
            // $proj.remove();
        }
    };

    $(".proj .dismiss_proj").on("click", dismiss_proj);
    //add new project to subject, select list show
    $(".add_proj").click(function () {
        var $list = $(this).next().find("select[name=addproj]");
        $list.slideToggle(400, function () {
            if ($list.is(":visible")) {
                var $group = $list.parentsUntil("form");
                $group.on("click", function (event) {
                    $list.slideUp(400, function () {
                        $group.off("click");
                    });
                });
            }
        });
    });


    //add new project to subject, click select list
    $("select[name=addproj]").click(function (event) {
        var title = $(event.target).text();
        var idp = $(event.target).val();
        var templet = $("#add_proj_templet").html();
        $proj = $(templet.replace(/projxxx/g, idp).replace(/projname/g, title));
        var $group = $("#projectsForm .part.proj div.tag");
        var judge = [];
        $group.each(function () {
            judge.push(this.innerHTML == title)
            // console.log(this.innerHTML)
        });
        res = true;
        for (j in judge) {
            if (judge[j]) {
                res = false;
                break;
            }
        }
        if (res) {
            $("div.addproj").before($proj);
            $proj.find(".dismiss_proj").on("click", dismiss_proj);
        } else {
            alert("This project is already added !")
            // console.log(title)
        }
    });


    // $.ajaxSetup({
    //     contentType: "application/x-www-form-urlencoded; charset=utf-8"
    // });
    // var formToJson = function (data) {
    //     data = data.replace(/&/g, "\",\"");
    //     data = data.replace(/=/g, "\":\"");
    //     data = "{\"" + data + "\"}";
    //     return data;
    // };
    // var data123 = $('#faaswfq').serialize(); //获取值
    // data123 = decodeURIComponent(data123, true); //防止中文乱码
    // var jsonx = formToJson(data123); //转化为json




});
