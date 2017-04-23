import tornado.ioloop
import tornado.web
import tornado
import pandas as pd
import wave
import StringIO
import os
import speech_recognition as sr

public_root = os.path.join(os.path.dirname(__file__), 'static')

title = "ASR GO Go with Leader B"

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("testWeb.html", title=title)

class FileHandler(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files
        # print "fileinfo is", fileinfo
        file_body = self.request.files['filearg'][0]['body']
        print("please say something")
        r = sr.Recognizer()
        #-------------------get audio------------------------
        with sr.AudioFile(StringIO.StringIO(file_body)) as source:
            audio = r.listen(source)
        try:
            print("analyse")
            out = r.recognize_google(audio,language="th-TH")
            self.write(out)
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
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    print("Started")
