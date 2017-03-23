#!/usr/bin/python
# encoding: utf-8

import os
import string
import sys
import workflow

from goto_validate import sanitizeNum

GITHUB_REPO = 'plongitudes/GoToMeetingTools'
UPDATE_FREQUENCY = 1

def main(wf):

    log.debug('Started')

    # set json as the serializer so that the phonebook is human readable (during debugging)
    # wf.data_serializer = 'json'

    if wf.stored_data('gotoPhonebook'):
        phonebook = wf.stored_data('gotoPhonebook')
    else:
        phonebook = []
        wf.add_item(
            title="GotoMeeting Address Book is empty",
            subtitle="Use the 'go add' keyword to add entries",
            icon=workflow.ICON_WARNING,
            valid=False
        )

    query = wf.args[1]
    valid_number = sanitizeNum(query)
    items = wf.filter(query, phonebook, key_for_entries)

    if (not items) and (valid_number is None) and (phonebook):
        wf.add_item(
            title="No matches found",
            icon=workflow.ICON_WARNING
        )
    elif (valid_number is not None):
        wf.add_item(
            title="Valid non-phonebook number",
            subtitle="Selecting this item will join the line above",
            arg=valid_number,
            icon=workflow.ICON_ACCOUNT,
            valid=True
        )
        wf.send_feedback()

    if wf.args[0] == "read" or wf.args[0] == "delete":
        for item in items:
            wf.add_item(
                title=item['desc'],
                subtitle=item['line'],
                arg=item['line'],
                valid=True
            )
        wf.send_feedback()

    elif wf.args[0] == "update":
        for item in items:
            wf.add_item(
                title=item['desc'],
                subtitle=item['line'],
                arg=item['desc'],
                valid=True
            )
        wf.send_feedback()

def key_for_entries(book):
    return '{} {}'.format(book['line'], book['desc'])

if __name__ == u"__main__":
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))

