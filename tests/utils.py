"""
:author: samu
:created: 2/21/13 12:01 AM
"""

import os
import shutil


class TestWithTmpdirMixin(object):
    def setUp(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ## yeah, I know that tmpnam is a potential security risk
            ## to my program, now STFU
            self.tmpdir = os.tmpnam()
        os.makedirs(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)
        del self.tmpdir
