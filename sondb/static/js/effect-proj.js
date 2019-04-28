$(document).ready(function () {

    // mark required items
    $("input:required").prev().addClass('mark');

    //delete proj or record
    $("a.del_proj").click(function () {
        var idp = $(this).prop("id");
        var pstate = $(this).attr('data-page-state');
        if (confirm("Sure to delete the item?")) {
            $.ajax({
                type: 'GET',
                url: "/projects/delete",
                data: {"idp": idp},
                success: function () {
                    if (pstate != "None") {
                        location.href = '/projects/overview/' + pstate;
                    } else {
                        location.href = '/projects/overview/all';
                    }
                },
                error: function (xhr) {
                    if (xhr.status == 400) {
                        location.href = '/projects/delete/error?e=more'
                    } else {
                        location.href = '/projects/delete/error?e=nop'
                    }
                }
            })
        }
    });


    $("input.single:checkbox").click(function () {
        var $it = $(this);
        var ischecked = $it.prop('checked');
        var domName = $it.attr("name");
        var domId = $it.attr("id");
        if (ischecked) {
            $("input[name=" + domName + "]").not("#" + domId).prop('checked', false);
        }
    });

    // show sublist
    $(".show_sublist input[name=isfinish]").click(function () {
        $.ajax({
            type: 'GET',
            url: "/projects/view/" + $(this).attr("data-idp") + "/search_subs",
            data: {isfinish: $(this).filter(":checked").val()},
            success: function (results) {
                $("section.subjectL").remove();
                $("section#proj_inform").after(results);
                $("section.subjectL").show("fast")
            }

        });

    });


});
