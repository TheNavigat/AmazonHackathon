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

function __log(e, data) {
    console.log(e + " " + (data || ''));
}

var audio_context;
var recorder;

function startUserMedia(stream) {
  var input = audio_context.createMediaStreamSource(stream);
  __log('Media stream created.');

  // Uncomment if you want the audio to feedback directly
  //input.connect(audio_context.destination);
  //__log('Input connected to audio context destination.');

  recorder = new Recorder(input);
  __log('Recorder initialised.');
}

function triggerRecording() {
    if (recorder.recording) {
        return stopRecording();
    }

    return startRecording();
}

function startRecording() {
  recorder && recorder.record();
  __log('Recording...');
}

function stopRecording() {
  recorder && recorder.stop();
  __log('Stopped recording.');

  // create WAV download link using audio data blob
  createDownloadLink();

  recorder.clear();
}

function createDownloadLink() {
  recorder && recorder.exportWAV(function(blob) {
    // var url = URL.createObjectURL(blob);
    // var li = document.createElement('li');
    // var au = document.createElement('audio');
    // var hf = document.createElement('a');

    // au.controls = true;
    // au.src = url;
    // hf.href = url;
    // hf.download = new Date().toISOString() + '.wav';
    // hf.innerHTML = hf.download;
    // li.appendChild(au);
    // li.appendChild(hf);
    // recordingslist.appendChild(li);
  });
}

window.onload = function init() {
  var thinkingtime = 30,
      display = document.getElementById("timer");

  thinkingTimer(thinkingtime, display);

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
