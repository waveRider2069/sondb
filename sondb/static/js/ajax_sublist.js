$(document).ready(function () {
    var $sub_consult_result = $("section.results");
    // var $p_group = $("#pagination #p_group");
    var $paging = $("#pagination");
    // var $page_temp = $('<div id="p_" class="p_cubic"></div>');
    // var pagination = function (pageN, p_index) {
    //     $p_group.empty();
    //     if (pageN <= 8) {
    //         for (p = 1; p <= pageN; p++) {
    //             var $page_cur = $page_temp.clone();
    //             $page_cur.prop("id", "p_" + p).text(p);
    //             if (p == p_index) {
    //                 $page_cur.addClass("p_cur")
    //             }
    //             $page_cur.appendTo($p_group)
    //         }
    //     } else {
    //         $page_temp.clone().prop("id", "p_" + p_index).text(p_index).addClass("p_cur").appendTo($p_group);
    //         //before
    //         var i = 1;
    //         while (p_index - i > 0 && i <= 4) {
    //             $page_temp.clone().prop("id", "p_" + (p_index - i)).text(p_index - i).prependTo($p_group);
    //             i++;
    //         }
    //         //after
    //         i = 1;
    //         while ((p_index + i <= pageN && i <= 4) || p_index + i <= 9) {
    //             if (i < 4 || p_index + i <= 8) {
    //                 $page_temp.clone().prop("id", "p_" + (p_index + i)).text(p_index + i).appendTo($p_group);
    //             } else {
    //                 $page_temp.clone().prop("id", "p_m").text("...").addClass("p_hint").removeClass("p_cubic").appendTo($p_group);
    //             }
    //             i++;
    //         }
    //     }
    //     if (p_index == 1) {
    //         $paging.find("#p_home, #p_pre").addClass("disabled")
    //     }
    //     if (p_index == pageN) {
    //         $paging.find("#p_next, #p_end").addClass("disabled")
    //     }
    //     $paging.find("#p_hint").text(pageN + " pages, go to");
    // };

    // consult result, sub-boxes, pages
    $sub_consult_result.show("fast");
    // var pageN = parseInt($sub_consult_result.attr("data-pages"));
    // var p_index = parseInt($sub_consult_result.attr("data-page"));
    // if (pageN > 0) {
    //     // pages
    //     pagination(pageN, p_index);
    // }
    $paging.find("div.p_static,div.p_cubic").not(".disabled, .p_cur").mousedown(function () {
        $(this).css({"background-color": "#199ED8"}).mouseup(function () {
            $(this).css({"background-color": "#fff"})
        })
    });
    $paging.find("div.p_static,div.p_cubic").not(".disabled, .p_cur").mouseleave(function () {
        $(this).css({"background-color": "#fff"})
    });


    // widgets
    var $slide_add_proj_w = $("section.results add_proj_w");
    var $slide_dismiss_proj_w = $("section.results dissmiss_proj_w");
    //  add_proj
    $slide_add_proj_w.click(function () {
        var $it = $(this).parent().siblings("select[name=addproj_w]");
        $it.slideToggle(function () {
            // var $group = $list.parentsUntil("form");
            $(document).on("click", function (event) {
                $it.slideUp(300, function () {
                    $(document).off("click");
                });
            });

        });

    });
    // dismiss_proj
    $slide_dismiss_proj_w.click(function () {
        var $it = $(this).parent().siblings("select[name=dismissproj_w]");
        $it.slideToggle(function () {
            $(document).on("click", function (event) {
                $it.slideUp(300, function () {
                    $(document).off("click");
                });
            });
        });
    });


});