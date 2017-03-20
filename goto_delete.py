#!/usr/bin/python
# encoding: utf-8

import json
import logging
import os
import string
import sys
import workflow
from workflow.notify import notify

log = None

def main(wf):

    log.debug('Started')

    # set json as the serializer so that the phonebook is human readable
    #wf.data_serializer = 'json'

    if wf.stored_data('gotoPhonebook'):
        phonebook = wf.stored_data('gotoPhonebook')
    else:
        phonebook = []

    # split args
    sane_query = wf.args[0].split()
    log.debug(sane_query)

    index = 0
    for item in phonebook:
        if item['line'] == sane_query[0]:
            # delete item from phonebook list
            matchline = item
            line = item['line']
            desc = item['desc']
            log.debug("deleting " + str(phonebook[index]) + ", index " + str(index) + ".")
            del phonebook[index]

            # write phonebook back out
            wf.store_data('gotoPhonebook', phonebook)
            notify(line + ": \"" + desc + "\" ", "Entry Deleted")

            # stop searching
            break
        else:
            index += 1
    else:
        matchline = {'line':None, 'desc':None}
        notify("nothing to delete: " + query)

    wf.send_feedback()


if __name__ == u"__main__":
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))

