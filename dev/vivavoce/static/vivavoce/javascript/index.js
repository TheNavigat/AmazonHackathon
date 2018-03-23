// TODO: SOME Clean up. Redundant code.
function thinkingTimer(duration, display) {
    var timer = duration, minutes, seconds;
    var interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.innerHTML= minutes + ":" + seconds;

        if (--timer < 0) {
            window.clearInterval(interval);
            talkingTimer(60,display);
        }
    }, 1000);
}

function talkingTimer(duration, display) {
    var timer = duration, minutes, seconds;
    interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.innerHTML= minutes + ":" + seconds;

        if (--timer < 0) {
            window.clearInterval(interval);
        }
    }, 1000);
}

function examDuration(duration, display) {
    var timer = duration, minutes, seconds;
    interval = setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.innerHTML= minutes + ":" + seconds;

        if (--timer < 0) {
            window.clearInterval(interval);
        }
    }, 1000);
}

window.onload = function () {
    var thinkingtime = 30,
        display = document.getElementById("timer");
    thinkingTimer(thinkingtime, display);
    var examTime = 60*45,
        durationDisplay = document.getElementById("duration");
    examDuration(examTime,durationDisplay);
    
};