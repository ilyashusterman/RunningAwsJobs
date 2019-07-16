import json
import logging
import os

import tornado.ioloop
import tornado.web

from job_managers.aws_job_manager import AwsJobManager

CLIENT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           'js_client'))
DEFAULT_FILENAME = 'test_filename.csv'
DEFAULT_BUCKET = 'test_job'


class MainHandler(tornado.web.RequestHandler):

    def initialize(self, aws_job_manager):
        super(MainHandler, self).initialize()
        self.aws_job_manager = aws_job_manager

    def post(self):
        s3_records = self.aws_job_manager.get_s3_records(
            filename=DEFAULT_FILENAME,
            bucket=DEFAULT_BUCKET
        )
        logging.info('Processing %s s3 records' % len(s3_records))
        s3_link_records_result = self.aws_job_manager.upload_records(s3_records)
        self.write(json.dumps({'s3_link_records_result': s3_link_records_result}))


class UIHandler(tornado.web.RequestHandler):
    def get(self):
        with open(os.path.join(CLIENT_PATH, 'jobs.html')) as f:
            self.write(f.read())


def make_app():
    aws_job_manager = AwsJobManager()
    return tornado.web.Application([
        (r"/api/process", MainHandler, dict(aws_job_manager=aws_job_manager)),
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