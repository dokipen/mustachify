import tornado.httpclient
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

import lxml.html
import os
import logging
import logging.config
import urlparse

import settings
import face

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger('mustachify.proxy')

from optparse import OptionParser

class HTTPProxyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self, url):
        source = "%s?%s" % (url, self.request.query)
        logger.debug('fetching %s' % source)

        def fn(res):
            logger.debug('got data')
            doc = lxml.html.document_fromstring(res.body)
            doc.make_links_absolute(url)
            for img in doc.xpath('//img'):
                if img.attrib.get('src'):
                    img.attrib['src'] = settings.IMG_PROXY % img.attrib['src']
            self.write(lxml.html.tostring(doc))
            self.finish()

        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(source, fn)

class ImageProxyHandler(tornado.web.RequestHandler):

    @tornado.web.asynchronous
    def get(self):
        url = self.request.arguments.get('url', [None])[0]
        if not url:
            raise ValueError('fuck you')

        result = face.find_faces(url)
        logger.debug('*********************')
        logger.debug(result)
        logger.debug('*********************')
        self.write('ok')
        self.finish()


url_mapping = [
    (r'/1/mustachify', ImageProxyHandler),
    (r'/1/(?P<url>.+)', HTTPProxyHandler),
]

app_settings = {
    "cookie_secret": "this_is_a_secret_cookie",
    "debug": False,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "autoescape": None,
}

if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog [options]",
                          version="0.1")

    parser.add_option("-p", "--port",
            action="store",
            dest="port",
            default="8000",
            help="Listening port",)

    (options, args) = parser.parse_args()

    application = tornado.web.Application(url_mapping, **app_settings)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(int(options.port))
    tornado.ioloop.IOLoop.instance().start()
