(function () {function __log(e, data) {
      log.innerHTML += "\n" + e + " " + (data || '');
    }

    var audio_context;
    var recorder;
    var rec = false;

    function startUserMedia(stream) {
      var input = audio_context.createMediaStreamSource(stream);
      // __log('Media stream created.');

      // Uncomment if you want the audio to feedback directly
      //input.connect(audio_context.destination);
      //__log('Input connected to audio context destination.');

      recorder = new Recorder(input);
      // __log('Recorder initialised.');
    }

    function decision(button) {
      if (rec===false) {
        rec = true;
        startRecording(button);
      } else if(rec === true){
        rec = false;
        stopRecording(button);
      }
    }

    function startRecording(button) {
      recorder && recorder.record();
      __log("Recording...");
    }

    function stopRecording(button) {
      recorder && recorder.stop();

      // create WAV download link using audio data blob
      createDownloadLink();

      recorder.clear();
      __log("Stop Recording.");
    }

    function createDownloadLink() {
      recorder && recorder.exportWAV(function(blob) {
        var formData = new FormData();
        formData.append("filearg", blob);
        var request = new XMLHttpRequest();
        request.open("POST", "/test");
        request.onload = function(oEvent) {
          if (request.status == 200) {
            __log(request.response);
            responsiveVoice.speak(request.response, "Thai Female");
          } else {
            __log("Error " + request.status + ".<br \/>");
          }
        };
        request.send(formData);
      });
    }

    window.onload = function init() {
      try {
        // webkit shim
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
        window.URL = window.URL || window.webkitURL;

        audio_context = new AudioContext;
        // __log('Audio context set up.');
        // __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
      } catch (e) {
        alert('No web audio support in this browser!');
      }

      navigator.getUserMedia({
        audio: true
      }, startUserMedia, function(e) {
        // __log('No live audio input: ' + e);
      });
    }
    
})();