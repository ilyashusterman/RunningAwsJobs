import os

import tornado.ioloop
import tornado.web

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'js_client'))


class MainHandler(tornado.web.RequestHandler):
    def post(self):
        self.write("Processing...")


class UIHandler(tornado.web.RequestHandler):
    def get(self):
        with open(os.path.join(CLIENT_PATH, 'jobs.html')) as f:
            self.write(f.read())


def make_app():
    return tornado.web.Application([
        (r"/api/process", MainHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler,
         {'path': CLIENT_PATH}),
        (r"/", UIHandler),
    ], debug=True)


if __name__ == "__main__":
    app = make_app()
    #TODO switch port to 80 (http) from test environment to production environment
    # app.listen(8888)
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()