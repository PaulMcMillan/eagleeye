========
eagleeye
========

EagleEye TE(4)

Installation
------------

* Install external dependencies:
 
  ``sudo apt-get install chromium-browser python-pip redis-server unzip xvfb``

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
