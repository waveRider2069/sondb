$(document).ready(function () {
    //submit new subject
    $("input.go[name=new_subject]").click(function () {
        var personalForm = $("form#personalForm").serialize();
        var hearingForm = $("form#hearingForm").serialize();
        var experimentForm = $("form#experimentForm").serialize();
        var commentsForm = $("form#commentsForm").serialize();
        var data1 = personalForm + "&" + hearingForm + "&" + experimentForm + "&" + commentsForm;
        // console.log(data1);
        $.ajax({
            type: 'POST',
            url: "/subject/creating",
            data: data1,
            success: function (resp) {
                location.href = '/subject/view/' + resp;
                // location.href = '/subject/view/' + resp;
            },
            error: function (xhr) {
                if (xhr.status == 400) {
                    location.href = '/subject/creating/error?e=noname';
                }
            }
        })
    });
    //delete subject


    //update subject
    $("input.go[name=update_subject]").click(function () {
        var personalForm = $("form#personalForm").serialize();
        var hearingForm = $("form#hearingForm").serialize();
        var commentsForm = $("form#commentsForm").serialize();
        var testsForm = $("form#testsForm").serialize();
        var projectsForm = $("form#projectsForm").serialize();
        var idr = $("select[name=record_date]").val();
        var record_date = $("select[name=record_date] option:selected").attr("data-date");
        var is_latest = $("select[name=record_date] option:selected").attr("data-latest");
        // data1 = testsForm;
        var data1 = personalForm + "&" + hearingForm + "&" + testsForm + "&" + projectsForm + "&" +
            commentsForm + "&record_date=" + record_date + "&is_latest=" + is_latest;
        // console.log(data1);
        $.ajax({
            type: 'POST',
            url: "/subject/view/" + idr + "/modifying",
            data: data1,
            success: function (resp) {
                location.href = '/subject/view/' + resp;
                // location.href = '/subject/view/' + resp;
            },
            error: function (xhr) {
                if (xhr.status == 400) {
                    location.href = '/subject/creating/error?e=noname';
                }
            }
        })
    });


    // switch recored
    $("select[name=record_date]").change(function () {
        var old_href = location.href;
        location.href = old_href.replace(/\/R[a-z,0-9]{12}/, "/" + $(this).val());
    })




});