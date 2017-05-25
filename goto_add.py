#!/usr/bin/python
# encoding: utf-8

import json
import logging
import os
import string
import sys
import workflow

from workflow.notify import notify
from util import sanitizeNum
from util import idGetter

import osascript_bug_patch

log = None

def main(wf):

    log.debug('Started')

    # set json as the serializer so that the phonebook is human readable (during debugging)
    # wf.data_serializer = 'json'

    # init some things
    action = ""
    number = 0
    nickname = ""
    sane_query = False

    if wf.stored_data('gotoPhonebook'):
        phonebook = wf.stored_data('gotoPhonebook')
    else:
        phonebook = []

    # split args
    query = wf.args[0].split()

    # and now sanity checks for the query
    log.debug(query)
    if (len(query) >= 3):
        flag = ""
        action = query[0]
        del query[0]
        # grab the last arg, it should be the number
        number = query[len(query)-1]
        
        # sanitize the number, starting with stripping out `-`s if present
        valid_number = sanitizeNum(number)
        if valid_number is None:
            flag = "not_num"
            # maybe the number was a url instead, we should grab the url id
            try:
                valid_number = idGetter(number)
            except ImportError:
                notify("Missing 'requests' Python module", "GotoMeeting Tools is missing a Python module. Please use pip or easy_install to install 'requests'")
                return

            if valid_number is None:
                flag = "not_url"
        log.debug(str(number) + " returned: " + str(valid_number))

        # we got something, let's use it.
        if valid_number is not None:
            # we don't need the last thing any more
            del query[len(query)-1]

            # what's left should be the description for the line
            nickname = query
            nickname = " ".join(nickname)
            # sanitize the name for storage
            valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
            valid_name = ''.join(c for c in nickname if c in valid_chars)

            sane_query = True
        else:
            if flag == "not_num":
                notify("No entry added", "The number you provided wasn't a valid GoToMeeting line. Make sure you provide both a description and a valid number.")
            elif flag == "not_url":
                notify("No entry added", "Something was wrong with the url you provided, it doesn't seem to lead to a valid GoToMeeting line.")
            else:
                notify("No entry added", "Not enough information provided. Make sure you provide both a description and a number.")
            return

    # is the query sane? let's move on.
    log.debug(str(sane_query))
    if (sane_query == True):
        if (str(action) == "create"):

            log.debug("starting create action")
                
            # check if the name is in the phonebook already
            for item in phonebook:
                if item['desc'] == valid_name:
                    matchname = item
                    break
            else:
                matchname = {'line':None, 'desc':None}
            
            # check if the number is in the phonebook already
            for item in phonebook:
                if item['line'] == valid_number:
                    matchline = item
                    break
            else:
                matchline = {'line':None, 'desc':None}
            
            log.debug(matchline)
            log.debug(matchname)

            if (matchline['line'] == valid_number) and (matchline['desc'] == valid_name):
                notify(valid_number + ": \"" + valid_name + "\"", "Duplicate, entry not added.")
            elif (matchline['line'] == valid_number):
                notify(valid_number + " already in the phonebook as \"" + matchline['desc'] + "\".", "Entry not added.")
            elif (matchname['desc'] == valid_name):
                notify(valid_name + " is already in the phonebook as \"" + matchname['line'] + "\".", "Entry not added.")
            else:
                phonebook.append({'line': valid_number, 'desc': valid_name})

                # write phonebook back out
                wf.store_data('gotoPhonebook', phonebook)
                notify(valid_number + ": \"" + valid_name + "\"", "Entry added.")

        elif (action == "override"):
            index = 0
            log.debug("looking for: " + str(wf.args))
            for item in phonebook:
                if item['desc'] == valid_name:
                    matchname = item
                    log.debug("found item: " + str(item) + " at index " + str(index))
                    break
                else:
                    index += 1
            else:
                matchname = {'line':None, 'desc':None}

            log.debug("match: " + str(matchname))
            log.debug("replacing: " + str(phonebook[index]) + " at index " + str(index))

            # with a valid match, let's rewrite the entry with the new number
            if (valid_number != None) and (item['desc'] != None):
                phonebook[index] = {'line': valid_number, 'desc':item['desc']}

                # write phonebook back out
                wf.store_data('gotoPhonebook', phonebook)
                notify(valid_number + ": \"" + valid_name + "\"", "Entry modified.")
            else:
                notify("Something went wrong", "Could not modify phonebook entry.")


    else:
        notify("No entry added", "Not enough arguments. Make sure you add a name and a number.")

    wf.send_feedback()

if __name__ == u"__main__":
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))

