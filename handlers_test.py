"""Unit tests for handlers.py.
"""

import json

import handlers
import models
import mox
import testutil
import webapp2

from google.appengine.ext import db


class HandlersTest(testutil.HandlerTest):

  def setUp(self):
    super(HandlersTest, self).setUp()
    handlers.SOURCES['fake'] = testutil.FakeSource
    self.source = testutil.FakeSource.new(self.handler)
    self.source.as_source.DOMAIN = 'fake.com'
    self.source.set_activities(
      [{'object': {
            'id': 'tag:fake.com,2013:000',
            'url': 'http://fake.com/000',
            'content': 'asdf http://orig/post qwert',
            }}])
    self.source.save()

  def check_response(self, url_template, expected):
    resp = handlers.application.get_response(url_template % self.source.key().name())
    self.assertEqual(200, resp.status_int, resp.body)
    header_lines = len(handlers.TEMPLATE.splitlines()) - 2
    actual = '\n'.join(resp.body.splitlines()[header_lines:-1])
    self.assert_equals(expected, actual)

  def test_get_post_html(self):
    self.check_response('/post/fake/%s/000', """\
<article class="h-entry">
<span class="u-uid">tag:fake.com,2013:000</span>
<div class="p-name"><a class="u-url" href="http://fake.com/000">asdf http://orig/post qwert</a></div>
<time class="dt-published" datetime=""></time>
<time class="dt-updated" datetime=""></time>

  <div class="e-content">
  asdf http://orig/post qwert

  </div>

</article>
""")

  def test_get_post_json(self):
    resp = handlers.application.get_response('/post/fake/%s/000?format=json' %
                                             self.source.key().name())
    self.assertEqual(200, resp.status_int, resp.body)
    self.assert_equals({
        'type': ['h-entry'],
        'properties': {
          'uid': ['tag:fake.com,2013:000'],
          'name': ['asdf http://orig/post qwert'],
          'url': ['http://fake.com/000'],
          'content': [{ 'html': 'asdf http://orig/post qwert',
                        'value': 'asdf http://orig/post qwert',
                        }],
          },
        },
        json.loads(resp.body))

  def test_post_bad_user(self):
    resp = handlers.application.get_response('/post/fake/not_a_user/000')
    self.assertEqual(400, resp.status_int)

  def test_post_bad_format(self):
    resp = handlers.application.get_response('/post/fake/%s/000?format=asdf' %
                                             self.source.key().name())
    self.assertEqual(400, resp.status_int)

  def test_get_comment_html(self):
    self.source.get_activities()[0]
    self.source.set_comment({
        'id': 'tag:fake.com,2013:111',
        'content': 'qwert',
        'inReplyTo': [{'url': 'http://fake.com/000'}],
        })

    self.check_response('/comment/fake/%s/000/111', """\
<article class="h-entry">
<span class="u-uid">tag:fake.com,2013:111</span>
<div class="p-name">qwert</div>
<time class="dt-published" datetime=""></time>
<time class="dt-updated" datetime=""></time>

  <div class="e-content">
  qwert

  </div>

<a class="u-in-reply-to" href="http://fake.com/000" />
<a class="u-in-reply-to" href="http://orig/post" />

</article>
""")

  def test_get_like_html(self):
    self.source.as_source.set_like({
        'objectType': 'activity',
        'verb': 'like',
        'id': 'tag:fake.com,2013:111',
        'object': {'url': 'http://example.com/original/post'},
        })

    self.check_response('/like/fake/%s/000/111', """\
<article class="h-entry h-as-like">
<span class="u-uid">tag:fake.com,2013:111</span>

<time class="dt-published" datetime=""></time>
<time class="dt-updated" datetime=""></time>

  <div class="e-content">
  likes this.
  <a class="u-like u-like-of" href="http://example.com/original/post" />
  <a class="u-like u-like-of" href="http://orig/post" />

  </div>

</article>
""")

  def test_get_repost_html(self):
    self.source.as_source.set_repost({
        'objectType': 'activity',
        'verb': 'share',
        'id': 'tag:fake.com,2013:111',
        'object': {'url': 'http://example.com/original/post'},
        })

    self.check_response('/repost/fake/%s/000/111', """\
<article class="h-entry h-as-repost">
<span class="u-uid">tag:fake.com,2013:111</span>

<time class="dt-published" datetime=""></time>
<time class="dt-updated" datetime=""></time>

  <div class="e-content">
  reposts this.
  <a class="u-repost u-repost-of" href="http://example.com/original/post" />
  <a class="u-repost u-repost-of" href="http://orig/post" />

  </div>

</article>
""")
