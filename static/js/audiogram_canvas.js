$(document).ready(function() {
    var canvas_r = document.getElementById('ctx_right');
    var ctx_r = canvas_r.getContext('2d');
    // console.log(ctx_r);

    var canvas_l = document.getElementById('ctx_left');
    var ctx_l = canvas_l.getContext('2d');
    // console.log(ctx_l);
    //
    // console.log($(canvas_r).height());
    //     console.log($(canvas_r).width());

    // ctx_r.fillRect(0,0,30,30);

    var min = $("input[name=thresh_left_250a]").prop("min");
    // console.log(min==-25)
    $(".go[value='Plot audiogram']").click(function() {
        var air_r = new Array();
        var bone_r = new Array();
        var air_l = new Array();
        var bone_l = new Array();
        var $thresh_air = $("div.air.panel .right input[type=range]");
        $thresh_air.each(function() {
            air_r.push($(this).val())
        });
        var $thresh_bone = $("div.bone.panel .right input[type=range]");
        $thresh_bone.each(function() {
            bone_r.push($(this).val())
        });
        var $thresh_air = $("div.air.panel .left input[type=range]");
        $thresh_air.each(function() {
            air_l.push($(this).val())
        });
        var $thresh_bone = $("div.bone.panel .left input[type=range]");
        $thresh_bone.each(function() {
            bone_l.push($(this).val())
        });

        // plot grid

        // plot bone right
        var isplot = false;
        for (b in bone_r) {
            if (bone[b] != min) {
                isplot = true;
                break;
            }
        }

    })


});