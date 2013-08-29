from itertools import takewhile

from eagleeye.precheck import PrecheckHTTP, PrecheckHTTPS

def test_precheck_http():
    qinput = PrecheckHTTP.qinput
    qoutput = PrecheckHTTP.qoutput
    qinput.clear()
    qoutput.clear()
    PrecheckHTTPS.qinput.clear()

    def send_job(host, port):
        qinput.send((host, port))
    
    send_job('httpbin.org', 80)
    send_job('httpbin.org', 443)
    send_job('httpbin.org', 8000)
    
    for job in takewhile(bool, PrecheckHTTP()):
        print job
    result = [x for x in takewhile(bool, qoutput)]
    assert result == ['http://httpbin.org:80']
    assert [x for x in takewhile(bool, PrecheckHTTPS.qinput)
            ] == [['httpbin.org', 443]]


def test_precheck_https():
    qinput = PrecheckHTTPS.qinput
    qoutput = PrecheckHTTPS.qoutput
    qinput.clear()
    qoutput.clear()

    def send_job(host, port):
        qinput.send((host, port))
    
    send_job('httpbin.org', 80)
    send_job('httpbin.org', 443)
    send_job('httpbin.org', 8000)

    for job in takewhile(bool, PrecheckHTTPS()):
        print job

    result = [x for x in takewhile(bool, qoutput)]
    assert result == ['https://httpbin.org:443']
