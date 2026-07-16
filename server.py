#!/usr/bin/env python3
"""博客服务器 - 强制UTF-8"""
import http.server, os, mimetypes

BLOG = os.path.expanduser("~/blog")

class BlogHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BLOG, **kwargs)

    def guess_type(self, path):
        t, _ = mimetypes.guess_type(path)
        return (t or 'text/html') + '; charset=utf-8'

if __name__ == '__main__':
    http.server.HTTPServer(('0.0.0.0', 8081), BlogHandler).serve_forever()
