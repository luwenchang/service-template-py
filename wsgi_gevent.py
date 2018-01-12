#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'vincent'

import os
import sys
import werkzeug.serving
from gevent.pywsgi import WSGIServer
from gevent.pool import Pool


from manage import app

reload(sys)
sys.setdefaultencoding("utf-8")



def start_dev(host="localhost", port=5000, workers=1):
    """启动服务 类型：Gevent WSGI Server"""

    app.debug=True
    @werkzeug.serving.run_with_reloader
    def run_server():
        http = WSGIServer(
            (host, port),
            app.wsgi_app,
            spawn=Pool(2)
        )

        http.serve_forever()

    run_server()

if __name__ == '__main__':
    start_dev()




