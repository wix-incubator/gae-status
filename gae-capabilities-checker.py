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
EXIT_CRITICAL   = 2
CAPABILITIES = ["blobstore",
                "datastore_v3",
                "images",
                "mail",
                "memcache",
                "taskqueue",
                "urlfetch",
                "xmpp"]

def parse_command_line():
    parser = optparse.OptionParser(version="%prog 1.5")
    parser.add_option("-n", "--name", dest="projectName", help="Project name ( e.g. wixarchive2)")
    parser.add_option("-p", "--path", dest="scriptPath", default=DEFAULT_PATH, help="path to the capabilities handler")
    parser.add_option("-X", "--exclude", dest="excluded", default=None, help="exclude capabilities <CAP-1>[|<CAP-2|...>]")
    parser.add_option("-c", "--capabilities", action="store_true", dest="capabilities", help="print list of capabilities")
    (options, args) = parser.parse_args()
    return options


def check_capabilities(project, script, exclude=None):
    url  = APPSPOT_ADDRESS % project
    if exclude:
        url += '%s?exclude=%s' % (script, exclude)
    else:
        url += script

    print url
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
    options = parse_command_line()
    if options.capabilities:
        print CAPABILITIES
        sys.exit(EXIT_GOOD)
    try:
        return_code, return_msg = check_capabilities(options.projectName, options.scriptPath, options.excluded)
        print return_msg
        sys.exit(return_code)
    except Exception, ex:
        print 'Failed on checking %s: %s' % (options.projectName, str(ex))
        sys.exit(EXIT_CRITICAL)

if __name__ == "__main__":
    main()