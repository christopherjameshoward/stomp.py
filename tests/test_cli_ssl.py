from stomp.__main__ import StompCLI
from .testutils import *


username = get_default_user()
password = get_default_password()

(sslhost, sslport) = get_ssl_host()[0]


class TestSSLCLI(object):

    def test_ssl(self):
        teststdin = StubStdin()
        teststdout = StubStdout(self)
        teststdout.expect("CONNECTED")

        cli = StompCLI(sslhost, sslport, username, password, "1.0", use_ssl=True, stdin=teststdin, stdout=teststdout)

        time.sleep(3)

        teststdout.expect("Subscribing to '/queue/testsubscribe' with acknowledge set to 'auto', id set to '1'")
        cli.onecmd("subscribe /queue/testsubscribe")
        teststdout.expect("MESSAGE")
        teststdout.expect("this is a test")
        cli.onecmd("send /queue/testsubscribe this is a test")

        time.sleep(3)

        teststdout.expect("Unsubscribing from '/queue/testsubscribe'")
        cli.onecmd("unsubscribe /queue/testsubscribe")
        teststdout.expect("Shutting down, please wait")
        cli.onecmd("quit")
