from eagleeye.selchrome import SeleniumWorker, WriteScreenshot

def test_base():
    worker = SeleniumWorker()
    worker.qinput.clear()
    worker.qoutput.clear()

    for url in ['http://google.com', 'http://comcast.net']:
        worker.qinput.send(url)

    job = True
    for job in worker:
        if not job:
            break
        print job

    worker = WriteScreenshot()
    for job in worker:
        if not job:
            break
        print(len(job))
