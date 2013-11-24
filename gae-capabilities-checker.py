#!/usr/bin/ python
#ecoding: utf-8
__author__ = 'artemk@wix.com'

import optparse
import urllib2
import time
import json
import sys

APPSPOT_ADDRESS = 'http://%s.appspot.com'
DEFAULT_PATH    = '/gae-capabilities'
EXIT_GOOD       = 0
EXIT_WARN       = 2
EXIT_CRITICAL   = 3


def parseCommandLine():
    parser = optparse.OptionParser(version="%prog 1.5")
    parser.add_option("-n", "--name", dest="projectName", help="Project name ( e.g. wixarchive2)")
    parser.add_option("-p", "--path", dest="scriptPath", default=DEFAULT_PATH, help="path to the capabilities handler")
    (options, args) = parser.parse_args()
    return options

"""
python2.6 /usr/lib/nagios/plugins/staticErrorsCount.py -s s0.aus.wixpress.com
NOK: sv(0) sv_http(0) lighty(41) vg(27) disp(0) dfstator(0) | supervisor=0;;100;;
supervisor_http=0;;200;; lighttpd=41;;40;; vangogh=27;;50;; dispatcher=0;;60;; dfstator=0;;70;;
"""
def check_capabilities(project, script):
    url  = APPSPOT_ADDRESS % project
    url += script
    text = urllib2.urlopen(url).read()
    result = json.loads(text)
    return_code = EXIT_CRITICAL
    return_msg  = ''

    if 'capabilities' in result:
        capabilities = result['capabilities']
        errors = 0
        for c in capabilities:
            status = EXIT_GOOD if capabilities[c]['is_enabled'] else EXIT_WARN
            if status != EXIT_GOOD:
                errors += 1
            return_msg += '%s(%s) ' % (c, status)

        if errors > 0:
            return_msg = 'NOK: %s' % return_msg
            return_code = EXIT_WARN
        else:
            return_msg = 'OK: %s' % return_msg
            return_code = EXIT_GOOD

    return return_code, return_msg,


def main():
    options = parseCommandLine()
    #try:
    return_code, return_msg = check_capabilities(options.projectName, options.scriptPath)
    print return_msg
    sys.exit(return_code)
    #except Exception, ex:
    #    print 'Failed on checking %s: %s' % (options.projectName, str(ex))
    #    sys.exit(3)

if __name__ == "__main__":
    main()