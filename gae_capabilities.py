#!/usr/bin/ python
#ecoding: utf-8
__author__ = 'artemk@wix.com'

import webapp2
import time
import json
from google.appengine.api import capabilities

CAPABILITIES = ["blobstore",
                "datastore_v3",
                ("datastore_v3", ["write"]),
                "images",
                "mail",
                "memcache",
                "taskqueue",
                "urlfetch",
                "xmpp"]


class GetCapabilities(webapp2.RedirectHandler):
    def __init__(self, request=None, response=None):
        super(GetCapabilities, self).__init__(request, response)

    def get(self):
        exclude  = self.request.get('exclude', None)
        callback = self.request.get('callback', None)
        if exclude:
            exclude = exclude.split('|')

        capability_dict = {}
        for c in CAPABILITIES:
            l = []
            k = c
            if isinstance(c, tuple):
                k = c[0]
                l = [c[1][0]]

            if exclude and k in exclude:
                continue

            cs = capabilities.CapabilitySet(k, l)
            d = {'is_enabled'   : cs.is_enabled(),
                 'admin_message': cs.admin_message()}
            k = k if len(l) < 1 else '%s__%s' % (k, l[0])
            capability_dict[k] = d

        response_json = {'capabilities': capability_dict,
                         'timestamp': time.time() * 1000}  # js ready timestamp
        self.response.headers['Content-Type'] = 'application/json'
        response_str = json.dumps(response_json)

        if callback:
            response_str = '%s(%s)' % (callback, response_str)

        return webapp2.Response.write(self.response, response_str)

app = webapp2.WSGIApplication([
    ('/gae-capabilities', GetCapabilities),
], debug=True)
