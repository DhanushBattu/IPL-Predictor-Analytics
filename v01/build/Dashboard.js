var video = document.getElementById("myVideo");
var btn = document.getElementById("myBtn");
var btn2 = document.getElementById("myBtn2");

function videoControl() 
{
    if (video.paused) {video.play(); btn.innerHTML = "Pause";} 
    else {video.pause(); btn.innerHTML = "Play";}
}

function nextPage()
{
    window.location.href = "http://localhost/Predictor/Selection.html";
}