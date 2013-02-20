"""
:author: samu
:created: 2/21/13 12:01 AM
"""

import os
import shutil
import subprocess


def run(args, silent=True):
    kwargs = {}
    if silent:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
    proc = subprocess.Popen(args, **kwargs)
    return proc.communicate()


class TestWithTmpdirMixin(object):
    def setUp(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ## yeah, I know that tmpnam is a potential security risk
            ## to my program, now STFU
            self.tmpdir = os.tmpnam()
        os.makedirs(self.tmpdir)
        self._prevdir = os.getcwd()
        os.chdir(self.tmpdir)

    def tearDown(self):
        os.chdir(self._prevdir)
        shutil.rmtree(self.tmpdir)
        del self.tmpdir

    def _rp(self, *args):
        return os.path.join(self.tmpdir, *args)

    def _open(self, name, mode='r'):
        return open(self._rp(name), mode)


class TestWithReadyTmpdirMixin(TestWithTmpdirMixin):
    def setUp(self):
        super(TestWithReadyTmpdirMixin, self).setUp()
        os.makedirs(self._rp('templates'))
        os.makedirs(self._rp('extra_templates'))
        os.makedirs(self._rp('data'))
        os.makedirs(self._rp('build'))

    def render(self):
        run(('confgen-render', '--root', self.tmpdir))
