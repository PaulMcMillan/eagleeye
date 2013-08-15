"""
Not amazing, but it's a start.
"""
import sys

import eagleeye


def run():
    if len(sys.argv) == 1:
        print "Pass a list space-separated urls."
        exit()
    qinput = eagleeye.Screenshot.qinput
    for arg in sys.argv[1:]:
        qinput.send(arg)
    print "Sent %s jobs" % (len(sys.argv) - 1)


if __name__ == '__main__':
    run()
