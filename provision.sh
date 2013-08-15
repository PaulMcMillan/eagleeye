#!/bin/bash
# get the latest setuptools
wget https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -O - | python
# install the latest pip
wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py -O - | python

# install our other dependencies
apt-get install chromium-browser unzip xvfb

# install chromedriver
curl https://chromedriver.googlecode.com/files/chromedriver_linux64_2.2.zip | funzip > chromedriver
chmod +x chromedriver
sudo mv chromedriver /usr/bin/chromedriver

# install eagleeye_te
sudo pip install eagleeye_te
