
// 시간 변환 함수
String.prototype.toHHMMSS = function () {
    var myNum = parseInt(this, 10);
    var hours   = Math.floor(myNum / 3600);
    var minutes = Math.floor((myNum - (hours * 3600)) / 60);
    var seconds = myNum - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}

let time01 = document.getElementById("conner_time");
time01.innerHtml.toHHMMSS();

// 팝업용 함수
// $(document).ready(function() {

//     $(".btn").click(function() {
//         $(".popup_bg").css({"display" : "block"});
//     });

//     $(".popup_bg").click(function() {
//         $(this).css({"display" : "none"});
//     });
// });


