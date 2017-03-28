#!/usr/bin/python
# encoding: utf-8

import json
import os
import string
import sys
import workflow
from workflow.notify import notify

from util import sanitizeNum

def main(wf):

    log.debug('Started')

    # set json as the serializer so that the phonebook is human readable (during debugging)
    # wf.data_serializer = 'json'

    # format phonebook so that Alfred can search it
    def key_for_entries(book):
        return '{} {}'.format(book['line'], book['desc'])

    # load up the phonebook
    if wf.stored_data('gotoPhonebook'):
        phonebook = wf.stored_data('gotoPhonebook')
    else:
        wf.add_item(
            title="GotoMeeting Address Book is empty",
            subtitle="Use the 'go add' keyword to add entries",
            icon=ICON_INFO
        )

    # get rid of the "update" part of the query so that we can match on a name
    valid_name = wf.args[0]
    valid_name.rstrip
    query_items = valid_name.split()
    del query_items[0]

    # now grab the new number off the end of the incoming information
    lastarg = len(query_items)-1
    number = query_items[lastarg]
    valid_number = None

    # but only if it's a complete number

    valid_number = sanitizeNum(number)
    if valid_number is not None:
    #if ((representsInt(number) == True) and (isMeetingNumber(number))):
        del query_items[lastarg]

    # let's make the valid_name again
    valid_name = " ".join(query_items)
    log.debug("valid_name follows")
    log.debug(valid_name)
    log.debug(valid_number)

    # give the user new instructions now that we're in a different script filter
    wf.add_item(
            title="Now add the new number for " + valid_name,
        subtitle="select the entry below when finished typing the new number.",
        icon=workflow.ICON_INFO
    )

    # gather applicable entry and add it to the menu
    items = wf.filter(valid_name, phonebook, key_for_entries)

    if not items:
        wf.add_item(
            title="No matches found",
            icon=workflow.ICON_INFO
        )

    for item in items:
        if valid_number:
            wf.add_item(
                title=item['desc'],
                subtitle=item['line'],
                arg=item['desc'] + " " + valid_number,
                valid=True
            )
    wf.send_feedback()

if __name__ == u"__main__":
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))

