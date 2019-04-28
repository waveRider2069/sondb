
// 获取窗口大小
var w=window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
var h=window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

window.screen.availHeight;   //可以不使用window前缀
window.screen.width;
window.screen.colorDepth;
window.screen.pixelDepth;

window.location.href;
window.location.hostname;
window.location.pathname;
window.location.port;
window.location.protocol;
window.location.hash;

window.location.assign("https://#");
window.location.reload();
window.location.replace("https://#");

window.history.forward();
window.history.back();
window.history.go();

window.alert();
window.prompt();
window.confirm();



var timer = window.setInterval();
var timer1 = window.setTimeout();
window.clearInterval();
window.clearTimeout();

document.cookie;
document.getElementById("out").htm