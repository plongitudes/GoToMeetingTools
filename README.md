# GoToMeetingTools
This is an Alfred 3 workflow meant to assist in managing GoToMeeting lines. Each phonebook entry is a valid GoToMeeting line number and a descriptor or name.

## General installation

- You'll need Alfred 3 installed with the PowerPack: http://www.alfredapp.com
- You'll need Python (which you should already have)
- Download the latest `GoToMeeting Tools.alfredworkflow` from the GitHub releases page at https://github.com/plongitudes/GoToMeetingTools/releases
- Double click the .alfredworkflow file to install it

## Usage Summary
- `go add <descriptor> <goto line #>`
- `go join <search pattern>`
- `go update <search pattern>`
- `go delete <search pattern>`
- `go backup`
- `go restore`
- `go import <filename>`

## Usage Details
- `go add`: is how you create new phonebook entries. The descriptor can be any combination of letters, numbers, and the following special characters: `_`, `.`, `(`, `)`, and ` `. Any other characters will be stripped.
- `go join`: is the method for launching a gotomeeting line. You can start searching on name or number, whichever you remember best :)
- `go update`: lets you modify any entry's phone number. The order of operations is:
    - type `go update` and start searching for the entry you want to modify. Once you have the right one, select it and hit enter.
    - The Alfred field will update with the entry name and look something like `go update Weekly Stand-up`.
    - Add the 9-digit GoToMeeting line number that you wish to be the new number for that entry.
    - Once the number is completely entered, the correct entry will appear in the list. Select it and hit enter; the entry will be modified accordingly.
- `go delete`: start typing to search for the entry you want to delete. Once it appears, select it and hit enter; that entry will be removed from the phonebook.
- `go backup`: create a backup in the user's home directory (`~/.gotoPhonebook`) of the internal cpickle datastore that is human readable. This is essentially a comma-separated csv that can be modified. This can also be used as a format guide for a valid `go import` action.
- `go restore`: overwrite the internal datastore with the contents of the backup in `~/.gotoPhonebook`.
- `go import`: import a file that replaces the current phonebook, or creates one if the user has no phonebook yet. The file must be a comma-separated csv in the form of `"123456789","Useful description goes here"`.

## TODO
- List all entries by default when searching
- allow entering a goto url and turning that into an entry
- Allow renaming of entries in addition to modifying line numbers
