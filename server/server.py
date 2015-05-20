#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import json
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from mongoengine import connect
from mongoengine import Document
from mongoengine import StringField, IntField


class OldTag(Document):
    tid = StringField()
    title = StringField()
    parentId = StringField()
    index = IntField()
    date = IntField()


class NewTag(Document):
    title = StringField()


class BookMark(Document):
    tid = StringField()
    index = IntField()
    parentId = StringField()
    title = StringField()
    url = StringField()
    date = IntField()


class OldTagHandler(RequestHandler):

    def post(self):
        data = json.loads(self.request.body)
        print data

        def save_tag(d):
            obj = OldTag()
            obj.tid = d.get('id', None)
            obj.title = d.get('title', None)
            obj.parentId = d.get('parentId', None)
            obj.index = d.get('index', None)
            obj.date = d.get('date', None)
            obj.save()
            return obj

        map(save_tag, data)
        self.finish('ok')


class NewTagHandler(RequestHandler):

    def get(self):
        data = OldTag.objects.all()

        title_list = list(set([d.title for d in data]))

        def tt(d):
            obj = NewTag()
            obj.title = d
            obj.save()
            return obj

        map(tt, title_list)
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

        self.finish(json.dumps(title_list))


class BookMarkHandler(RequestHandler):
    def post(self):
        data = json.loads(self.request.body)

        def save_mark(mark):
            obj = BookMark()
            obj.tid = mark.get('id', None)
            obj.title = mark.get('title', None)
            obj.url = mark.get('url', None)
            obj.date = mark.get('date', None)
            obj.index = mark.get('index', None)
            obj.save()
            return obj

        map(save_mark, data)


if __name__ == "__main__":
    connect('test_chrome')
    app = Application([
        ('/old_tag', OldTagHandler),
        ('/new_tag', NewTagHandler),
        ('/bookmark', BookMarkHandler),
    ], debug=True)
    app.listen(8001)

    ioloop = IOLoop.instance()
    print "listening on 8001"
    ioloop.start()
