// TODO: SOME Clean up. Redundant code.
var answerInterval;
var questioncount;
function thinkingTimer(duration, display) {
    var timer = duration, minutes, seconds;
    answerInterval = setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.innerHTML= minutes + ":" + seconds;

        if (--timer < 0) {

            startRecording();
        }
    }, 1000);
}

function talkingTimer(duration, display) {
    var timer = duration, minutes, seconds;
    answerInterval = setInterval(function () {
        minutes = parseInt(timer / 60, 10)
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.innerHTML= minutes + ":" + seconds;

        if (--timer < 0) {
            stopRecording();
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

function __log(e, data) {
    console.log(e + " " + (data || ''));
}

var audio_context;
var csrftoken = Cookies.get('csrftoken');
var recorder;
console.log(csrftoken);
function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  __log('Media stream created.');

  // Uncomment if you want the audio to feedback directly
  //input.connect(audio_context.destination);
  //__log('Input connected to audio context destination.');

  recorder = new Recorder(input);
  __log('Recorder initialised.');
}


function triggerRecording(id,count) {
    if (recorder['recording']) {
        console.log("id is " + id + " out of "+count);
        if(id<count){
        questioncount = count;
        }
        return stopRecording();
    }
    return startRecording();
}

function startRecording() {
  recorder && recorder.record();
  document.getElementById("micimage").src = "/../static/vivavoce/images/micred.png";
  window.clearInterval(answerInterval);
  talkingTimer(60,display);
  __log('Recording...');
}

function stopRecording() {
  recorder && recorder.stop();
  document.getElementById("micimage").src = "/../static/vivavoce/images/mic.png";
  window.clearInterval(answerInterval);
  __log('Stopped recording.');


  // create WAV download link using audio data blob
  uploadRecording();
  recorder.clear();
}

function uploadRecording() {
  recorder && recorder.exportWAV(function(blob) {
    var formData = new FormData();
    formData.append("file", blob);

    var request = new XMLHttpRequest();

    // TODO: Handle failures
    request.open("POST", "/upload/" + TEST_ID + "/" + QUESTION_ID + "/");
    request.setRequestHeader("X-CSRFToken", csrftoken);
    request.send(formData);

    if(questioncount != null)
      window.location.replace("/start/" + TEST_ID + "/" + (QUESTION_ID + 1) + "/");
    else
      window.location.replace("/thankyou/"+ TEST_ID+"/"+ QUESTION_ID+"/");
  });
}

function rekognize(path, id){
  var formData = new FormData();
  formData.append('path',path);
  formData.append('id',id);

  var request = new XMLHttpRequest();

  request.open("POST","/rekognize/");
  request.setRequestHeader("X-CSRFToken", csrftoken);
  request.send(formData);


}

var thinkingtime = 30,
    display = document.getElementById("timer");

window.onload = function init() {
  var examTime = 60*45,
      durationDisplay = document.getElementById("duration");

  examDuration(examTime,durationDisplay);

  try {
    // webkit shim
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
    window.URL = window.URL || window.webkitURL;

    audio_context = new AudioContext;
    __log('Audio context set up.');
    __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
  } catch (e) {
    alert('No web audio support in this browser!');
  }

  navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
    __log('No live audio input: ' + e);
  });
};
