import httplib
import logging
import socket

import requests
import requests.exceptions
import requests.packages.urllib3.exceptions

from tasa.store import Queue
from tasa.worker import BaseWorker

CONNECTION_TIMEOUT = 10


logger = logging.getLogger(__name__)

class PrecheckHTTP(BaseWorker):
    qinput = Queue('precheck:http') # (hostname, port)
    qoutput = Queue('image:http')

    def run(self, job):
        hostname, port = job
        http_url = 'http://%s:%s' % (hostname, port)

        try:
            r = requests.get(http_url, timeout=CONNECTION_TIMEOUT,
                             verify=False)
        
        except requests.exceptions.ConnectionError as e:
            if type(e.message) == requests.packages.urllib3.exceptions.SSLError:
                pass # we don't speed this flavor of ssl
            if (hasattr(e.message, 'reason') and
                type(e.message.reason) == httplib.BadStatusLine):
                PrecheckHTTPS.qinput.send(job)  # likely HTTPS
            elif (hasattr(e.message, 'reason') and
                  type(e.message.reason) == socket.error and
                  hasattr(e.message.reason, 'errno')):
                errno = e.message.reason.errno
                if errno == 111:  # Connection Refused
                    pass  # don't try to keep talking to closed port
                elif errno == 104:  # Connection reset by peer
                    PrecheckHTTPS.qinput.send(job)  # likely HTTPS
        except requests.exceptions.Timeout:
            pass  # don't try to keep talking to an unresponsive server
        except socket.timeout:
            # requests shouldn't be raising this should it?
            pass   # don't try to keep talking to an unresponsive server
        except Exception as e:
            logger.debug("Unhandled PrecheckHTTP %s %s", type(e), e.message)
            pass
        else:
            if r.status_code < 400:
                yield r.request.url  # goes to qoutput
            elif r.status_code == 400:
                # HTTPS servers sometimes respond with 400 errors to plain HTTP
                PrecheckHTTPS.qinput.send(job)  # likely HTTPS


class PrecheckHTTPS(BaseWorker):
    qinput = Queue('precheck:https')
    qoutput = Queue('image:http')

    def run(self, job):
        hostname, port = job
        https_url = 'https://%s:%s' % (hostname, port)

        try:
            r = requests.get(https_url, timeout=CONNECTION_TIMEOUT,
                             verify=False)
        except requests.exceptions.SSLError as e:
            pass  # This doesn't speak HTTPS we can understand
        except requests.exceptions.ConnectionError as e:
            pass  # This doesn't want to talk to us
        except request.exceptions.Timeout:
            pass  # don't mess with this, it takes too long
        except socket.timeout:
            # requests shouldn't be raising this should it?
            pass   # don't try to keep talking to an unresponsive server
        except Exception as e:
            logger.debug("Unhandled PrecheckHTTPS %s %s", type(e), e.message)
            pass
        else:
            if r.status_code < 400:
                yield r.request.url  # to qoutput


class PrecheckTCP(BaseWorker):
    """ Does a synack. Not particularly efficient."""
    qinput = Queue('precheck:tcp')
    #qoutput = Queue('')  # Subclass this to send output somewhere useful

    def run(self, job):
        hostname, port = job
        try:
            socket.create_connection((hostname, port), CONNECTION_TIMEOUT)
        except socket.timeout:
            pass
        except socket.error as e:
            pass
        else:
            socket.close()
            yield job
