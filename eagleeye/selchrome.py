import base64
import httplib
import logging
import os
import socket

import pyvirtualdisplay
import selenium.common
import selenium.common.exceptions
import selenium.webdriver.chrome.service as chrome_service

from selenium import webdriver

from tasa.store import Queue
from tasa.worker import BaseWorker


logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.INFO)
SOCKET_TIMEOUT = 30


class SeleniumWorker(BaseWorker):
    qinput = Queue('image:http')
    qoutput = Queue('result:save_image')

    _driver = None
    _service = None

    def __init__(self, socket_timeout=SOCKET_TIMEOUT, *args, **kwargs):
        super(SeleniumWorker, self).__init__(*args, **kwargs)

        # set up the xvfb display
        self.display = pyvirtualdisplay.Display(visible=0, size=(1280, 1024))
        self.display.start()

        # NOTE: This DOES change the socket timeout globally. There's
        # not much we can do about that though, since we don't have
        # access to the offending socket buried deeply in urllib2.

        # set socket timeout to kill hung chromedriver connections
        self.original_socket_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(socket_timeout)

        # Set up the webdriver options
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--disable-java')
        self.options.add_argument('--incognito')
        self.options.add_argument('--use-mock-keychain')
        #options.add_argument('--kiosk')
        # http://peter.sh/experiments/chromium-command-line-switches/

    @property
    def service(self):
        if self._service is None:
            self._service = chrome_service.Service('chromedriver')
            self._service.start()
        return self._service

    @property
    def driver(self):
        if self._driver is None:
            self._driver = webdriver.Remote(
                self.service.service_url,
                desired_capabilities=self.options.to_capabilities())
            # These timeout commands don't presently work with
            # chromedriver (v23). Leaving them in in case the
            # chromedriver people suddenly fix this issue:
            # https://code.google.com/p/chromedriver/issues/detail?id=9
            self._driver.set_script_timeout(15)
            self._driver.implicitly_wait(15)
            try:
                self._driver.set_page_load_timeout(15)
            except selenium.common.exceptions.WebDriverException:
                # this is for backwards compatibility with non 2.x
                # chromedriver releases.
                pass
        return self._driver

    def terminate_driver(self):
        """ Things go wrong with the webdriver; we want to recover robustly """
        logger.info('Terminating webdriver.')
        # Don't quit the driver here because it often hangs
        self._driver = None
        if self._service is not None:
            proc = self._service.process
            try:
                self._service.stop()
                proc.kill()
                # pgroup = os.getpgid(self._service.process.pid)
                # os.killpg(pgroup, ) # XXX
            except Exception:
                # This is really bad...
                pass
        # throw away the old one no matter what
        self._service = None

    def dismiss_alerts(self):
        # handle any possible blocking alerts because selenium is stupid
        alert = self.driver.switch_to_alert()
        try:
            alert.dismiss()
            logger.info(
                'Closed alert for %s: %s', self.driver.current_url, alert.text)
        except selenium.common.exceptions.NoAlertPresentException:
            pass

    def run(self, job):
        target_url = job
        logger.info('Loading %s', target_url)
        screenshot = None
        driver = self.driver
        try:
            driver.get(target_url)
            self.dismiss_alerts()
            logger.debug('Loaded %s' % target_url)

            screenshot = driver.get_screenshot_as_base64()

            # try going to a blank page so we get an error now if we can't
            driver.get('about:blank')
        except socket.timeout:
             logger.info('Terminating overtime connection: %s', target_url)
             self.terminate_driver()
        except (selenium.common.exceptions.WebDriverException,
                httplib.BadStatusLine):
            # just kill it, alright?
            self.terminate_driver()
        except Exception as e:
            print repr(e)
            print 'MAJOR PROBLEM: ', target_url
            self.terminate_driver()
        if screenshot:
            yield [screenshot, target_url]
            logger.debug('Finished %s', target_url)

    def __del__(self):
        socket.setdefaulttimeout(self.original_socket_timeout)
        self.terminate_driver()
        self.display.stop()


class WriteScreenshot(BaseWorker):
    qinput = Queue('result:save_image')

    def run(self, job):
        """ Separate task (and queue: write_screenshot) for writing the
        screenshots to disk, so it can be run wherever the results are
        desired.
        """
        # This code could be much cleaner. It was copied wholesale
        # from the old project.
        screenshot, url = job
        binary_screenshot = base64.b64decode(screenshot)
        file_name = url.replace(':', '_').replace('/', '_')
        file_path = os.path.join(os.getcwd(), 'out/%s.png' % file_name)
        with open(file_path, 'w') as f:
            f.write(binary_screenshot)

