$(document).ready(function () {
    //submit search conditions
    // $("input.go[name=search_subject]").click(function () {
    //     var personalForm = $("form#personalForm").serialize();
    //     var hearingForm = $("form#hearingForm").serialize();
    //     var experimentForm = $("form#experimentForm").serialize();
    //     var commentsForm = $("form#commentsForm").serialize();
    //     var data1 = personalForm + "&" + hearingForm + "&" + experimentForm + "&" + commentsForm;
    //     // console.log(data1);
    //     $.ajax({
    //         type: 'POST',
    //         url: "/consult/search",
    //         data: data1,
    //         success: function (resp) {
    //
    //             // location.href = '/subject/view/' + resp;
    //             // location.href = '/subject/view/' + resp;
    //         },
    //         error: function (xhr) {
    //             // if (xhr.status == 400) {
    //             //     location.href = '/subject/creating/error?e=noname';
    //             // }
    //         }
    //     })
    // });
    var getCondition = function () {
        var personalForm = $("form#personalForm").serialize();
        var hearingForm = $("form#hearingForm").serialize();
        var experimentForm = $("form#experimentForm").serialize();
        var keys = $("form#searchBox input[name=keywords]").val();
        var data1 = "cond=init";
        var unfold = [0, 0, 0];
        var slideid = '';
        var folders = ['hearf=1', 'personf=1', 'experf=1'];
        if (hearingForm !== 'conduction=air') {
            unfold[0] = 1;
            data1 = data1 + "&" + hearingForm;
        }
        if (personalForm) {
            unfold[1] = 1;
            data1 = data1 + "&" + personalForm;
        }
        if (experimentForm) {
            unfold[2] = 1;
            data1 = data1 + "&" + experimentForm;
        }
        $(".ui-slider-handle").each(function () {
            if ($(this).text()) {
                slideid = $(this).attr("id");
                if (slideid.startsWith('f')) {
                    unfold[0] = 1
                } else if (slideid.startsWith('age')) {
                    unfold[1] = 1
                }
                data1 = data1 + '&' + $(this).attr("id") + "=" + $(this).text()
            }
        });
        data1 = data1 + '&keys=' + encodeURIComponent(keys);
        console.log(data1);
        for (i in folders) {
            if (unfold[i]) {
                data1 = data1 + '&' + folders[i]
            }
        }
        return data1
    };
    var $sub_consult_result = $("section.results");
    var pageN = parseInt($sub_consult_result.attr("data-pages"));
    var p_index = parseInt($sub_consult_result.attr("data-page"));
    var changepage = function (page) {
        var path = '/consult/search?';
        var condition = getCondition();
        var sort = $("form.sort input[name=sort]:checked").val();  // 1 for latest, 2 for earliest, 3 for HL desc, 4 for HL asc
        if (!sort) {
            sort = "1";
        }

        path = path + "sort=" + sort + "&page=" + page + "&" + condition + "#focus";
        location.href = path;
    };

    $("#pagination").find("div.p_cubic, div.p_static").not(".disabled, .p_cur").click(function () {
        var pid = $(this).attr("id");
        var page = 1;
        if (pid === "p_pre") {
            page = Math.max(p_index - 1, 1)
        } else if (pid === "p_next") {
            page = Math.min(p_index + 1, pageN)
        } else if (pid === "p_end") {
            page = pageN
        } else if (pid === "p_go") {
            page = parseInt($("#pagination input#p_input").val());
            if (page) {
                page = Math.min(Math.max(1, page), pageN)
            } else {
                page = 1
            }
        } else {
            page = $(this).text()
        }
        changepage(page.toString())
    });

    $("form.sort input[name=sort]").change(function () {
        var path = '/consult/search?';
        var condition = getCondition();
        var sort = $(this).val();
        path = path + "sort=" + sort + "&" + condition + "#focus";
        location.href = path;
    });


    $("input.go[name=search_subject]").click(function () {
        var path = '/consult/search?';
        var condition = getCondition();
        path = path + "sort=1" + "&" + condition + "#focus";
        location.href = path;
    });

    $("form#searchBox").submit(function (event) {
        event.preventDefault();
        $("input.go[name=search_subject]").trigger("click")

    })

});