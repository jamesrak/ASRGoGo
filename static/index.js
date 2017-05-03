function __log(e, data, talk) {
  if(talk)
    log.innerHTML += '<div class = "row message">' + (data || '') + '</div>';
  else
    log.innerHTML += '<div class = "row message right_talk">' + (data || '') + '</div>';
  var myDiv = $("#log").get(0);
  myDiv.scrollTop = myDiv.scrollHeight;
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
}

function stopRecording(button) {
  recorder && recorder.stop();

  // create WAV download link using audio data blob
  createDownloadLink();

  recorder.clear();
}

function createDownloadLink() {
  recorder && recorder.exportWAV(function(blob) {
    var formData = new FormData();
    formData.append("filearg", blob);
    var request = new XMLHttpRequest();
    request.open("POST", "/recog");
    request.onload = function(oEvent) {
      if (request.status == 200) {
        __log(0, request.response, false);
        $.ajax({
          url: '/response',
          type: 'POST',
          data: JSON.stringify({ text: 'ฉัน อยาก ตื่น ห้า โมง'})
        })
        .done(function(response) {
          console.log(response);

          __log(0, response, true);
          responsiveVoice.speak(response, "Thai Female");
        })

      } else {
        __log(0,"โกวาจีกำลังเอ๋อง่ะ<div style=\"margin-top: -5px; font-size: 0.6em; font-weight: 200; color: #666;\">ERROR CODE " + request.status + "</div>", true);
        var xxxxx = Math.random();
        if(xxxxx < 0.33) responsiveVoice.speak("พูดอะไรของเธอน่ะ", "Thai Female" , {pitch: pp}, {rate: 1.7});
        else if(xxxxx > 0.66) responsiveVoice.speak("บ่นบ่นบ่น", "Thai Female" , {pitch: pp}, {rate: 1.7});
        else responsiveVoice.speak("งงค่ะ", "Thai Female" , {pitch: pp}, {rate: 1.7});
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

function scrollToBottom(id){
  var div = document.getElementById(id);
  div.scrollTop = div.scrollHeight - div.clientHeight;
}


////////////////////////////////////////////////////////

var width, height, largeHeader, canvas, ctx, triangles, target, animateHeader = true;
var colors = ['255,100,224', '100,183,225', '118,245,100', '244,105,102', '141,102,245' ,
 '253,225,119', '255,255,255', '128,222,250'];
var sw = -90;
var toggle = false;
var aph = 0.5;
var neww = true;

function startTri(){
    if(toggle === false && neww){
        toggle = true;
        aph = 0.5;
        neww = false;
        initHeader();
        addListeners();
        initAnimation();
    } else if(toggle === false && !neww){
        aph = 0.5;
        toggle = true;
    } else {toggle = false; aph = 0;}
    console.log(toggle);
}

function initHeader() {
    width = window.innerWidth;
    height = window.innerHeight;
    target = {x: 0, y: height};

    largeHeader = document.getElementById('large-header');
    largeHeader.style.height = height+'px';

    canvas = document.getElementById('demo-canvas');
    canvas.width = width;
    canvas.height = height;
    ctx = canvas.getContext('2d');

    // create particles
    triangles = [];
    for(var x = 0; x < 400; x++) {
        addTriangle(x*30);
    }
}

function addTriangle(delay) {
    setTimeout(function() {
        var t = new Triangle();
        triangles.push(t);
        tweenTriangle(t);
    }, delay);
}

function initAnimation() {
    animate();
}

function tweenTriangle(tri) {
    var t = Math.random()*(2*Math.PI);
    var x = (200+Math.random()*100)*Math.cos(t) + width*0.5;
    var y = (200+Math.random()*100)*Math.sin(t) + height+sw;
    var time = 10+4*Math.random();

    TweenLite.to(tri.pos, time, {x: x,
        y: y, ease:Circ.easeOut,
        onComplete: function() {
            tri.init();
            tweenTriangle(tri);
    }});
}

// Event handling
function addListeners() {
    window.addEventListener('scroll', scrollCheck);
    window.addEventListener('resize', resize);
}

function scrollCheck() {
    if(document.body.scrollTop > height) animateHeader = false;
    else animateHeader = true;
}

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    largeHeader.style.height = height+'px';
    canvas.width = width;
    canvas.height = height;
}

function animate() {
    if(animateHeader) {
        ctx.clearRect(0,0,width,height);
        for(var i in triangles) {
            triangles[i].draw();
        }
    }
    requestAnimationFrame(animate);
}

// Canvas manipulation
function Triangle() {
    var _this = this;

    // constructor
    (function() {
        _this.coords = [{},{},{}];
        _this.pos = {};
        init();
    })();

    function init() {
        _this.pos.x = width*0.5;
        _this.pos.y = height+sw;
        _this.scale = 0.1+Math.random()*0.5;
        _this.color = colors[Math.floor(Math.random()*colors.length)];
        setTimeout(function() { _this.alpha = aph; }, 5);
    }

    this.draw = function() {
        if(_this.alpha >= 0.005) _this.alpha -= 0.005;
        else _this.alpha = 0;
        ctx.beginPath();
        ctx.arc(_this.pos.x, _this.pos.y, _this.scale*30, 0, 2 * Math.PI, false);
        ctx.fillStyle = 'rgba('+_this.color+','+ _this.alpha+')';
        ctx.fill();
    };

    this.init = init;
}
