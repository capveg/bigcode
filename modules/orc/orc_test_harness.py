#!/usr/bin/python

"""
Testing harness for Open Route Cache ("orc")

Connect to a set of switches (possibly via ssh, possibly locally),
Take as input one or more pairs of wires, e.g., switch1:orc_i <--> switch2:orc_j
Assign orcXX interfaces IP addresses and routes
And then do what we can to confirm routing works with ping, etc.

Leverage the unittesting framework
"""

import argparse
import os
import pexpect
import sys
import unittest



class SwitchControl(object):
    """ The control connection to a switch shell

    Either over ssh (remotely) or bash (locally)
    """
    def __init__(self, host=None, user=None, verbose=False, logfile=None):
        """
        @param host if None, local connection, else hostname
        @param user if host is a hostname, then what user to ssh as
        """
        self.host = host
        self.user = user if user is not None else os.environ['USER']
        self.local = host == None
        self.verbose = verbose
        if self.local:
            self.channel = pexpect.spawn('bash',logfile=logfile)
            self.name = 'local'
        else:
            ssh_cmd = "ssh %s@%s" % (self.user, host)
            self.log("Spawning '%s'..." % ssh_cmd) 
            self.channel = pexpect.spawn("ssh %s@%s" % (self.user, host),logfile=logfile)
            self.name = host

    def testChannel(self):
        """ Run the echo command on the control and verify it returns correctly"""
        teststr = 'ORC IS GREAT'
        self.sendline("echo %s" % teststr)
        self.expect(teststr)
        return True

    def sendline(self, s=''):
        """ Send a line to the channel """
        if self.verbose:
            self.log("%s << %s" % (self.name, s))
        self.channel.sendline(s)

    def expect(self, pattern, timeout=-1, searchwindowsize=-1):
        """ Expect a pattern from the channel """
        if self.verbose:
            self.log("%s !! %s" % (self.name, pattern))
        ret = self.channel.expect(pattern, timeout, searchwindowsize)
        if self.verbose:
            s = self.channel.before
            if type(self.channel.after) == type('str'):
                s +=  self.channel.after 
            for line in s.split('\r\n'):
                    self.log("%s >> %s" % (self.name, line))
        return ret

    def log(self,s):
        sys.stderr.write("%s\n" % s)

    def close(self):
        self.channel.close()

    def ping(self, ip = '8.8.8.8' , iface=None, timeout = 5):
        """ Ping ip and return True or False if reachable """
        pattern = "64 bytes from %s" % ip
        self.sendline("ping -n %s" % ip)
        return 0 == self.expect([ pattern, pexpect.TIMEOUT] , timeout = timeout)
         


 

class TestSelfTest(unittest.TestCase):
    """ Verify the testing harness itself """

    def setUp(self):
        host = None
        logfile = None
        #logfile = sys.stderr
        #host='sbs3.hw.bigswitch.com'
        self.local_switch = SwitchControl(host, logfile=logfile)
        #self.local_switch.verbose = True

    def test_local_channel(self):
        self.assertTrue(self.local_switch.testChannel())

    def test_ping_google(self):
        self.assertTrue(self.local_switch.ping('8.8.8.8'))

    def test_ping_fail(self):
        self.assertFalse(self.local_switch.ping('255.255.255.0'))
        
    def tearDown(self):
        self.local_switch.close()


if __name__ == '__main__':
    ap = argparse.ArgumentParser("Open Route Cache Test Harness",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    ap.add_argument("--selftest", help="Force test harness selftest",
                    action='store_true')
    ap.add_argument("--prefix", help="IP CIDR prefix for dummy addresses",
                    default="10.234")
    ops = ap.parse_args()

    testsuite = unittest.TestSuite()
    if ops.selftest:
            testsuite.addTest( unittest.makeSuite(TestSelfTest))
    unittest.TextTestRunner(descriptions=True, verbosity=2).run( testsuite)

