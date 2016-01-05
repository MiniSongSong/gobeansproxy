# coding: utf-8
import telnetlib
from tests.dbclient import MCStore
from tests.base import BaseTest


class AbnormalCmdTest(BaseTest):
    def setUp(self):
        BaseTest.setUp(self)
        self.invalid_key = '/this/is/a/bad/key/%s' % chr(15)

    def run_cmd_by_telnet(self, cmd, expected, timeout=2):
        addr, port = self.proxy.addr.split(':')
        t = telnetlib.Telnet(addr, port)
        t.write('%s\r\n' % cmd)
        out = t.read_until('\n', timeout=timeout)
        t.write('quit\n')
        t.close()
        r = out.strip('\r\n')
        self.assertEqual(r, expected)

    def test_get(self):
        # get not exist key
        cmd = 'get /test/get'
        self.run_cmd_by_telnet(cmd, 'END')

        # invalid key
        cmd = 'get %s' % self.invalid_key
        self.run_cmd_by_telnet(cmd, 'END')
        self.checkCounterZero()

    def test_set(self):
        # invalid key
        cmd = 'set %s 0 0 3\r\naaa' % self.invalid_key
        self.run_cmd_by_telnet(cmd, 'SERVER_ERROR write failed')

        cmd = 'set /test/set 0 0 3\r\naaaa'
        self.run_cmd_by_telnet(cmd, 'CLIENT_ERROR bad data chunk')
        self.checkCounterZero()

    def test_delete(self):
        key = '/delete/not/exist/key'
        cmd = 'delete %s' % key
        self.run_cmd_by_telnet(cmd, 'NOT_FOUND')

        cmd = 'delete %s' % self.invalid_key
        self.run_cmd_by_telnet(cmd, 'NOT_FOUND')
        self.checkCounterZero()

    def test_get_meta_by_key(self):
        key = '/get_meta_by_key/not/exist/key'
        cmd = 'get ?%s' % key
        self.run_cmd_by_telnet(cmd, 'END')

        cmd = 'get ?%s' % self.invalid_key
        self.run_cmd_by_telnet(cmd, 'END')
        self.checkCounterZero()
