$(document).ready(function () {

    $("form.pick_state input[name='state']").click(function () {
        location.href = '/projects/overview/' + $(this).val()
    })

});