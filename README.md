# GoToMeetingTools
This is an Alfred 3 workflow meant to assist in managing GoToMeeting lines. Each phonebook entry is a valid GoToMeeting line number and a descriptor or name.

## General installation

- You'll need Alfred 3 installed with the PowerPack: http://www.alfredapp.com
- You'll need Python (which you should already have)
- Download the latest `GoToMeeting Tools.alfredworkflow` from the GitHub releases page at https://github.com/plongitudes/GoToMeetingTools/releases
- Double click the .alfredworkflow file to install it

## Usage Summary
- `go add <descriptor> <goto line # | http://gotomeet.me/customurl>`
- `go join <search pattern>`
- `go update <search pattern>`
- `go delete <search pattern>`
- `go share <search pattern`
- `go backup`
- `go restore`
- `go import <filename>`

## Usage Details
- `go add`: is how you create new phonebook entries. The descriptor can be any combination of letters, numbers, and the following special characters: `_`, `.`, `(`, `)`, and ` `. Any other characters will be stripped.
    - `go add <description> <gotomeeting line number>`: line number here should be in the form of `111222333` or `111-222-333`.
    - `go add <description> <gotomeeting url>`: urls like `http://gotomeet.me/customurl` will be converted into a line number and added to the phonebook.
- `go join`: is the method for launching a gotomeeting line. You can start searching on name or number, whichever you remember best :)
- `go update`: lets you modify any entry's phone number. The order of operations is:
    - type `go update` and start searching for the entry you want to modify. Once you have the right one, select it and hit enter.
    - The Alfred field will update with the entry name and look something like `go update Weekly Stand-up`.
    - Add the 9-digit GoToMeeting line number that you wish to be the new number for that entry.
    - Once the number is completely entered, the correct entry will appear in the list. Select it and hit enter; the entry will be modified accordingly.
- `go delete`: start typing to search for the entry you want to delete. Once it appears, select it and hit enter; that entry will be removed from the phonebook.
- `go share <search pattern>`: Share a meeting URL. This is in the form of `Join my GotoMeeting: https://global.gotomeeting.com/host/111222333`, and is both copied to the clipboard and pasted into the foreground window. The pasting behavior can be altered in the "Copy to Clipboard" node in the workflow.
- `go backup`: create a backup in the user's home directory (`~/.gotoPhonebook`) of the internal cpickle datastore that is human readable. This is essentially a comma-separated csv that can be modified. This can also be used as a format guide for a valid `go import` action.
- `go restore`: overwrite the internal datastore with the contents of the backup in `~/.gotoPhonebook`.
- `go import`: import a file that replaces the current phonebook, or creates one if the user has no phonebook yet. The file must be a comma-separated csv in the form of `"123456789","Useful description goes here"`.

## TODO
- handle webinars
- Allow renaming of entries in addition to modifying line numbers

## Release Notes
- 1.2.0: Turn a gotomeet.me url into a phonebook entry
    - Added: New entry adding functionality, url instead of line number: `go add <description> <http://gotomeet.me/customname>` will now fetch a meeting number and turn it into a phonebook entry.

- 1.1.2: Sharing is Caring (and reading is fun)
    - Added: ability to share a gotomeeting url from alfred.
    - Added: the full phonebook is now listed by default if the query is empty.

- 1.1.0: Backup/restore, plus joining lines without an entry
    - Added ability to backup the phonebook from internal cpickle format
    - Added ability to restore from said backup
    - Added ability to (destructively) import a comma-separated csv in the form of "line","description" for new users.
    - Added ability to join a line if you have no current entry for that line: `go join 123456789` will be a selectable menu item once the line number entered is deemed valid (9-digit line)
    - Lastly, externalized some sanitization functions to keep code more lean.

- 1.0.3: Fixed issue with "update" not working
    - The update action was clobbering the wrong entry on update, this is now fixed.

- 1.0.2: allow numbers with dashes
    - Added better line number handling for gotomeeting lines (usually they're displayed as xxx-xxx-xxx, this is now handled correctly)

- 1.0.1
    - initial release with basic CRUD functionality
