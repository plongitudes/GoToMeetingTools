# GoToMeetingTools
This is an Alfred 3 workflow meant to assist in managing GoToMeeting lines. Each phonebook entry is a valid GoToMeeting line number and a descriptor or name.

## General installation

- You'll need Alfred 3 installed with the PowerPack: http://www.alfredapp.com
- You'll need Python (which you should already have)
- Download the latest `GoToMeeting Tools.alfredworkflow` from the GitHub releases page at https://github.com/plongitudes/GoToMeetingTools/releases
- Double click the .alfredworkflow file to install it

## Usage Summary
- go add <descriptor> <goto line #>
- go join <search pattern>
- go update <search pattern>
- go delete <search pattern>

## Usage Details
- `go add`: is how you create new phonebook entries. The descriptor can be any combination of letters, numbers, and the following special characters: `_`, `.`, `(`, `)`, and ` `. Any other characters will be stripped.
- `go join`: is the method for launching a gotomeeting line. You can start searching on name or number, whichever you remember best :)
- `go update`: lets you modify any entry's phone number. The order of operations is:
    - type `go update` and start searching for the entry you want to modify. Once you have the right one, select it and hit enter.
    - The Alfred field will update with the entry name and look something like `go update Weekly Stand-up`.
    - Add the 9-digit GoToMeeting line number that you wish to be the new number for that entry.
    - Once the number is completely entered, the correct entry will appear in the list. Select it and hit enter; the entry will be modified accordingly.
- `go delete`: start typing to search for the entry you want to delete. Once it appears, select it and hit enter; that entry will be removed from the phonebook.

## TODO
- List all entries by default when searching
- Allow renaming of entries in addition to modifying line numbers
- Create import/export option for adding or modifying many entries at once
