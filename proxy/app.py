import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

from optparse import OptionParser

class ProxyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('hello world')

url_mapping = [
    (r'/1/(?P<url>.+)', ProxyHandler),
]

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options]",
                          version="0.1")
    (options, args) = parser.parse_args()

    application = tornado.web.Application(url_mapping, **app_settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(int(options.port))
    tornado.ioloop.IOLoop.instance().start()
