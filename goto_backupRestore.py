#!/usr/bin/python
# encoding: utf-8

import csv
import logging
import os
import sys
import string
import workflow

from workflow.notify import notify
from util import sanitizeNum

import osascript_bug_patch

log = None

def main(wf):

    log.debug('Started')
    log.debug(wf.args)
    query = wf.args[0].split()

    if (query[0] == "import"):
        backup_phonebook = query[1]
        log.debug(backup_phonebook)
    else:
        backup_phonebook = os.path.expanduser("~") + "/.gotoPhonebook"

    def convertToCSV(list):
        csv_data = []
        #for item in list:
            
    if (query[0] == "backup"):
        if wf.stored_data('gotoPhonebook'):
            phonebook = wf.stored_data('gotoPhonebook')

            with open(backup_phonebook, 'wb') as phonebook_fh:
                writer = csv.writer(phonebook_fh, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
                for item in phonebook:
                    newrow = [item['line'], item['desc']]
                    writer.writerow(newrow)

            notify("Backup successful.", "Phonebook backup created in " + str(backup_phonebook))
        else:
            notify("Unable to backup!", "Couldn't read cpickle phonebook, please restore from a previous backup.")

    if (query[0] == "restore") or (query[0] == "import"):
        if os.path.isfile(backup_phonebook):
            phonebook = []

            with open(backup_phonebook, 'rb') as phonebook_fh:
                backup_data = csv.reader(phonebook_fh)
                for row in backup_data:
                    phonebook.append({'line': row[0], 'desc': row[1]})
                    log.debug(str(phonebook))

            # write phonebook back out
            wf.store_data('gotoPhonebook', phonebook)

            if (query[0] == "backup"):
                notify("Restored from backup!", "Restored from " + str(backup_phonebook))
            else:
                notify("Imported phonebook!", "Imported from " + str(backup_phonebook))
        else:
            if (query[0] == "backup"):
                notify("Unable to read backup!", "Couldn't read phonebook backup.")
            else:
                notify("Unable to read import file!", "Couldn't read csv.")


    wf.send_feedback()


if __name__ == u"__main__":
    wf = workflow.Workflow()
    log = wf.logger
    sys.exit(wf.run(main))

