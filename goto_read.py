#!/usr/bin/python
# encoding: utf-8

import os
import string
import sys
import workflow

from util import sanitizeNum

def main(wf):

    log.debug('Started')

    # set json as the serializer so that the phonebook is human readable (during debugging)
    # wf.data_serializer = 'json'

    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item(
            title="New version available",
            subtitle="Select this menu item to install the update",
            autocomplete="workflow:update",
            icon=workflow.ICON_INFO
        )

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
    log.debug("query = wf.args[1]: " + str(query))
    # check to see if the user is typing a valid number,
    # in case they want to join a meeting for which they have no entry
    valid_number = sanitizeNum(query)

    if (len(query) == 0):
        items = []
        for item in phonebook:
            if wf.args[0] == "update":
                arg_output = item['desc']
            else:
                arg_output = item['line']
            wf.add_item(
                title=item['desc'],
                subtitle=item['line'],
                arg=arg_output,
                valid=True
            )
        wf.send_feedback()
    else:
        # and look up what they're typing also.
        items = wf.filter(query, phonebook, key_for_entries)

        # user might be typing in a meeting number that we don't have an entry for
        if (len(query) > 0 ) and (not items) and (valid_number is None) and (phonebook):
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
    wf = workflow.Workflow(
            update_settings={
                'github_slug': 'plongitudes/GoToMeetingTools',
                'frequency': 1
                }
            )
    log = wf.logger
    sys.exit(wf.run(main))

