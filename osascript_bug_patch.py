#!/usr/bin/python
# encoding: utf-8

import os
import webbrowser
import platform

# get around https://bugs.python.org/issue30392 in macOS 10.12.5
if platform.uname()[0] == 'Darwin' and platform.mac_ver()[0] == '10.12.5':
    def monkey_func(self, url, new=0, autoraise=True):
        if self._name == 'default':
            script = 'do shell script "open %s"' % url.replace('"', '%22')  # opens in default browser
        else:
            script = '''
               tell application "%s"
                   activate
                   open location "%s"
               end
               ''' % (self._name, url.replace('"', '%22'))
        osapipe = os.popen("osascript", "w")
        if osapipe is None:
            return False
        osapipe.write(script)
        rc = osapipe.close()
        return not rc

    webbrowser.MacOSXOSAScript.open = monkey_func

