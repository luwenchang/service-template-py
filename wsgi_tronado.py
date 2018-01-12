#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vincent'

import sys

from manage import app

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import  IOLoop


reload(sys)
sys.setdefaultencoding("utf-8")



http_server = HTTPServer(WSGIContainer(app))
http_server.listen(5000)
IOLoop.instance().start()