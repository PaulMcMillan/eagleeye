#!/bin/bash

# update our package list
sudo apt-get update

# install our dependencies
sudo apt-get -y install chromium-browser python-pip redis-server unzip xvfb

# install chromedriver
curl https://chromedriver.googlecode.com/files/chromedriver_linux64_2.2.zip | funzip > chromedriver
chmod +x chromedriver
sudo mv chromedriver /usr/bin/chromedriver

# install eagleeye_te
sudo pip install eagleeye_te
