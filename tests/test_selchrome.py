from eagleeye.selchrome import SeleniumWorker, WriteScreenshot

def test_base():
    worker = SeleniumWorker()

    for url in ['http://google.com', 'http://comcast.net']:
        worker.qinput.send(url)

    job = True
    while job:
        job = worker().next()
        print job

    worker = WriteScreenshot()
    job = True
    while job:
        job = worker().next()


