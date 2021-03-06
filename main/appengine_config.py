# coding: utf-8

import os
import sys

from path_util import sys_path_insert

# lib.zip has been precompiled from the gulp tasks when running inside of the Google Environment 
# in the first case use the copy of lib.zip that has been pre-compiled
if os.environ.get('SERVER_SOFTWARE', '').startswith('Google App Engine'):
  sys_path_insert('lib.zip')
# in the case when running locally compile lib.zip on demand
else:
  if os.name == 'nt':
    os.name = None
    sys.platform = ''

  import re
  from google.appengine.tools.devappserver2.python import runtime

  try:
    re_ = runtime.stubs.FakeFile._skip_files.pattern.replace('|^lib/.*', '')
    re_ = re.compile(re_)
    runtime.stubs.FakeFile._skip_files = re_
  except AttributeError:
    # runtime.stubs doesn't exist in the test environment
    pass
  sys_path_insert('lib')

sys_path_insert('libx')


def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app
