# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2011, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Neil Soman neil@eucalyptus.com
#         Mitch Garnaat mgarnaat@eucalyptus.com

from boto.roboto.awsqueryrequest import AWSQueryRequest
from boto.roboto.param import Param
import euca2ools.commands.euare

class GetLdapSyncStatus(AWSQueryRequest):

    ServiceClass = euca2ools.commands.euare.Euare

    Description = """GetLdapSyncStatus"""
    Params = []
    Response = {u'type': u'object', u'name': u'GetLdapSyncStatusResponse',
                u'properties': [{
        u'doc': u' Contains the result of a successful invocation of the GetLdapSyncStatus action. ',
        u'type': u'object',
        u'name': u'GetLdapSyncStatusResult',
        u'optional': False,
        u'properties': [{
            u'doc': u' A flag that indicates whether LDAP sync is enabled',
            u'optional': False,
            u'name': u'SyncEnabled',
            u'type': u'boolean',
            }, {
            u'doc': u' A flag that indicates whether LDAP sync is in progress',
            u'optional': False,
            u'name': u'InSync',
            u'type': u'boolean',
            }],
        }, {
        u'type': u'object',
        u'optional': False,
        u'name': u'ResponseMetadata',
        u'properties': [{u'type': u'string', u'optional': False, u'name': u'RequestId'}],
        }]}

    def cli_formatter(self, data):
        print "SyncEnabled\t", data.SyncEnabled
        print "InSync\t", data.InSync
            
    def main(self, **args):
        return self.send()

    def main_cli(self):
        self.do_cli()