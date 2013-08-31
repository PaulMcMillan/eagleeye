#!/usr/bin/env python
"""
A script which searches Shodan and pipes the results into eagleeye for
screenshotting. This script is meant as an example, not a fully baked
tool. Expand on it and change things as they suit your needs.

You're responsible for making sure you're sending it something
reasonable to screenshot, it's not this script's fault if you point
your browsers at a bunch of SSH services.

Usage:
$mkdir out
$chmod +X shodfeed.py
$export SHODAN_API_KEY=A12E3C56787...
$tasa eagleeye:PrecheckHTTP
$tasa eagleeye:PrecheckHTTPS
$tasa eagleeye:Screenshot &
$tasa eagleeye:Writer &
$./shodfeed.py your_query_here
"""
import logging
import os
import sys

import shodan

import eagleeye


logger = logging.getLogger('shodfeed')
logging.basicConfig(level=logging.DEBUG)

def get_shodan_result(query, api_key, page=1):
    logger.info("Fetching shodan results query: %s page: %s", query, page)
    api = shodan.WebAPI(api_key)
    try:
        res = api.search(query, page=page)
    except shodan.api.WebAPIError:
        logger.info('Finished shodan results with %s page(s).', page - 1)
    else:
        for r in res.get('matches', []):
            t = (r['ip'], r['port'])
            logger.debug('Sending: %s %s', *t)
            eagleeye.PrecheckHTTP.qinput.send(t)
        return res.get('matches', [])


if __name__ == '__main__':
    try:
        api_key = os.environ['SHODAN_API_KEY']
    except KeyError:
        try:
            api_key = open('SHODAN_API_KEY').read()
        except IOError:
            print ("Put your shodan API key in the environment with\n"
                   "export SHODAN_API_KEY=yourkeyhere\n"
                   "or put your key in a file named SHODAN_API_KEY.")
            exit()

    page = 1
    while get_shodan_result(' '.join(sys.argv[1:]), api_key, page):
        page += 1
