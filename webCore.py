import tornado.ioloop
import tornado.web
import tornado
import wave
import io
import os
import speech_recognition as sr
import http
import json
from client import speechToText
import pickle
import wave
from utilities.response_text import generateResponseText

public_root = os.path.join(os.path.dirname(__file__), 'static')

title = "ASR GO Go with Leader B"

#----------------------make frequency dataset from words-----------------------------------
def token(x):
    return x.split(' ')

#-----------------------read model------------------------------
model = pickle.load(open("dev/clf.sav","rb"))
countT = pickle.load(open("dev/countT.sav","rb"))
print(generateResponseText('โกวาจี',0))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("testWeb.html", title=title)

def getJSONResponse(audio):
    BODY = audio
    conn = http.client.HTTPConnection("localhost", 8080)
    conn.request("PUT", "/client/dynamic/recognize", BODY)
    try:
        response = conn.getresponse()
        string = response.read().decode('utf-8')
        json_response = json.loads(string)
        print(json_response)
        return str(json_response['hypotheses'][0]['utterance'])
    except Exception as e:
        print("Error: " + str(e))
        return str(e)

class RecogHandler(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files
        file_body = self.request.files['filearg'][0]['body']
        r = sr.Recognizer()
        #-------------------get audio------------------------
        with sr.AudioFile(io.BytesIO(file_body)) as source:
            audio = r.listen(source)
        try:
            print("analyse")
            # out = getJSONResponse(file_body)
            # print(type(file_body))
            # print(type(audio.get_raw_data()))
            f = wave.open(io.BytesIO(file_body), 'r')
            out = speechToText(f)
            # out = r.recognize_google(audio,language="th-TH")
            self.write(out)
        except sr.RequestError as e:
            self.write("Could not understand audio")

class ResponseHandler(tornado.web.RequestHandler):
    def post(self):
        out = tornado.escape.json_decode(self.request.body)
        df = [out['text']]
        count = countT.transform(df)
        y_pred = model.predict(count)
        print(out['text'])
        print(y_pred[0])
        tell = generateResponseText(out['text'], y_pred[0])
        print(tell)
        self.write(tell)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/recog", RecogHandler),
        (r"/response", ResponseHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': public_root}),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(4000)
    tornado.ioloop.IOLoop.current().start()
    print("Started")
