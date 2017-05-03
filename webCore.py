import tornado.ioloop
import tornado.web
import tornado
import wave
import io
import os
import speech_recognition as sr
import http
import json
import pickle
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

class FileHandler(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files
        # print "fileinfo is", fileinfo
        file_body = self.request.files['filearg'][0]['body']
        print("please say something")
        r = sr.Recognizer()
        #-------------------get audio------------------------
        with sr.AudioFile(io.BytesIO(file_body)) as source:
            audio = r.listen(source)
        try:
            print("analyse")
            out = r.recognize_google(audio,language="th-TH")
            # out = getJSONResponse(file_body)
            df = [out]
            count = countT.transform(df)
            y_pred = model.predict(count)
            tell = generateResponseText(out,y_pred)
            self.write(tell)
        except sr.RequestError as e:
            self.write("Could not understand audio")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/test", FileHandler),
        (r'/(.*)', tornado.web.StaticFileHandler, {'path': public_root}),
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(4000)
    tornado.ioloop.IOLoop.current().start()
    print("Started")
