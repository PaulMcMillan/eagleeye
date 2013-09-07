========
eagleeye
========

EagleEye TE(4)

Installation
------------

* Install external dependencies:
 
  ``sudo apt-get install -y chromium-browser python-pip redis-server unzip xvfb``

* Install chromedriver:
 
  | ``curl https://chromedriver.googlecode.com/files/chromedriver_linux64_2.2.zip | funzip > chromedriver``
  | ``chmod +x chromedriver``
  | ``sudo mv chromedriver /usr/bin/chromedriver``

* Install eagleeye itself:
 
  ``sudo pip install eagleeye_te``

Usage
-----

* Start some eagleeye workers:
 
  | ``tasa eagleeye:Screenshot &``
  | ``mkdir -p out``
  | ``tasa eagleeye:Writer &``
   
* And feed the system a job:
 
  ``eagleeye http://google.com``


Notes
-----

If you're using Kali linux or Debian, unfortunately there are
compatibility problems with the latest pre-built version of
chromedriver. You can try using an older version from here:

https://chromedriver.googlecode.com/files/chromedriver_linux64_23.0.1240.0.zip

If you're using Kali, please go interact with this bug so that the
Kali linux maintainers know that people want to use a new version of
chromedriver:

http://bugs.kali.org/view.php?id=527
