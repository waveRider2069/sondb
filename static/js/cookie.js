function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}


function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function checkCookie() {
    var username = getCookie("username");
    if (username != "") {
        alert("Welcome again " + username);
    } else {
        username = prompt("Please enter your name:", "");
        if (username != "" && username != null) {
            setCookie("username", username, 365);
        }
    }
}

function localstore() {
    if (typeof(Storage) !== "undefined") {
        localStorage.sitename = "菜鸟教程";
        document.getElementById("result").innerHTML = "网站名：" + localStorage.sitename;
    } else {
        document.getElementById("result").innerHTML = "对不起，您的浏览器不支持 web 存储。";
    }
}


function json_method() {
    var text = '{ "name":"Runoob", "initDate":"2013-12-14", "site":"www.runoob.com"}';
    var obj = JSON.parse(text, function(key, value) {
        if (key == "initDate") {
            return new Date(value);
        } else {
            return value;
        }
    });
    document.getElementById("demo").innerHTML = obj.name + "创建日期：" + obj.initDate;

}

function json_method1() {
    var text = '{ "name":"Runoob", "initDate":"2013-12-14", "site":"www.runoob.com"}';
    var obj = JSON.parse(text);
    obj.initDate = new Date(obj.initDate);

    document.getElementById("demo").innerHTML = obj.name + "创建日期: " + obj.initDate;
}


