# Copyright 2009-2014 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import pipes
import sys

from euca2ools.commands.sts import STSRequest
from requestbuilder import Arg, MutuallyExclusiveArgList


class GetImpersonationToken(STSRequest):
    DESCRIPTION = 'Get a token for impersonation of a user'
    ARGS = [Arg('-a', '--account-name', dest='AccountAlias', metavar='ACCOUNT',
                required=True,
                help='alias for the account (required)'),
            Arg('-u', '--user-name', dest='UserName', metavar='USER',
                required=True,
                help='name of the user (required)'),
            Arg('-d', '--duration', dest='DurationSeconds', metavar='SECONDS',
                type=int, default=900, help='''number of seconds the
                credentials should be valid for (900-3600) (default: 900)'''),
            MutuallyExclusiveArgList(
                Arg('-c', dest='csh_output', route_to=None,
                    action='store_true', help='''generate C-shell commands on
                    stdout (default if SHELL looks like a csh-style shell'''),
                Arg('-s', dest='sh_output', route_to=None,
                    action='store_true', help='''generate Bourne shell
                    commands on stdout (default if SHELL does not look
                    like a csh-style shell'''))]

    def print_result(self, result):
        creds = result['Credentials']
        # If this list changes please go update ReleaseRole.
        self.__print_var('AWS_ACCESS_KEY_ID', creds['AccessKeyId'])
        self.__print_var('AWS_ACCESS_KEY', creds['AccessKeyId'])
        self.__print_var('EC2_ACCESS_KEY', creds['AccessKeyId'])
        self.__print_var('AWS_SECRET_ACCESS_KEY', creds['SecretAccessKey'])
        self.__print_var('AWS_SECRET_KEY', creds['SecretAccessKey'])
        self.__print_var('EC2_SECRET_KEY', creds['SecretAccessKey'])
        self.__print_var('AWS_SESSION_TOKEN', creds['SessionToken'])
        self.__print_var('AWS_SECURITY_TOKEN', creds['SessionToken'])
        self.__print_var('AWS_CREDENTIAL_EXPIRATION', creds['Expiration'])
        self.__print_var('EC2_USER_ID', self.params['AccountAlias'])
        # Unset AWS_CREDENTIAL_FILE to avoid accidentally using its creds
        self.__print_var('AWS_CREDENTIAL_FILE', None)
        print
        print '# If you can read this, rerun this program with eval:'
        print '#     eval `{0}`'.format(
            ' '.join(pipes.quote(arg) for arg in sys.argv))

    def __print_var(self, key, val):
        if (self.args.get('csh_output') or
                (not self.args.get('sh_output') and
                 os.getenv('SHELL', '').endswith('csh'))):
            if val:
                fmt = 'setenv {key} {val};'
            else:
                fmt = 'unsetenv {key};'
        else:
            if val:
                fmt = '{key}={val}; export {key};'
            else:
                fmt = 'unset {key};'
        print fmt.format(key=key, val=val)

