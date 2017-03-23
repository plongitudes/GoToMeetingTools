#!/usr/bin/python
# encoding: utf-8

import string
import logging

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

def sanitizeNum(input_number):
    valid_chars = (string.digits)
    number = ''.join(c for c in input_number if c in valid_chars)
    if representsInt(number) and isMeetingNumber(number):
        return number
    else:
        return None

