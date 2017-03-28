#!/usr/bin/python
# encoding: utf-8

import logging
import re
import requests
import string

# two small funcs to validate gotomeeting numbers
def representsInt(some_string):
    try:
        int(some_string)
        return True
    except ValueError:
        return False

def isMeetingNumber(some_string):
    if ((representsInt(some_string)) and (len(some_string) == 9)):
        return True
    else:
        return False

# test if a series of digits _could_ be a GoToMeeting meeting.
# if so, strip hyphens if present
def sanitizeNum(input_number):
    valid_chars = (string.digits)
    number = ''.join(c for c in input_number if c in valid_chars)
    if representsInt(number) and isMeetingNumber(number):
        return number
    else:
        return None

# pull html from a gotomeeting url and get line number
def idGetter(url):
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)
    # request the page contents
    log.debug("url: " + str(url))
    regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|' # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)' # ...or ipv6
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    url_match = regex.match(url)

    log.debug(url_match)

    if url_match is not None:
        html = requests.get(url).text
    else:
        return None

    empty = 0
    found_href = []
    goto_line = ""

    while empty == 0:
        # go until we find an href
        curpos = html.find("href")
        if curpos >= 0:
            # we found an href
            htmllen = len(html)
            # slice it up a little
            html = html[curpos:htmllen]
            curpos = html.find('"')
            htmllen = len(html)
            html = html[curpos+1:htmllen]
            curpos = html.find('"')
            needle = html[0:curpos]
            if needle.startswith("http" or "www"):
                found_href.append(needle)
        else:
            empty = 1

    # examine each url for a meeting line
    for item in found_href:
        words = re.findall(r"[\w']+", item)
        if "global" in words:
            for word in words:
                if sanitizeNum(word) is not None:
                    goto_line = word
                    break

    if goto_line is not "":
        return goto_line
    else:
        return None

