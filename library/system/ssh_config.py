#!/usr/bin/python

# Copyright (c) 2016 crito <crito@fnordpipe.org>

DOCUMENTATION = '''
---
module: ssh_config
short_description: manage (user specific) ssh config
description:
    - manage (user specific) ssh config
options:
    user:
        description:
            - name of the user to manage config
        required: False
        default: null
    option:
        description:
            - The option to modify
        required: True
        default: null
    value:
        description:
            - set the option field to this value
        required: True
        default: null
requirements:
    - 'python >= 2.6 # OS package'
'''

EXAMPLES = '''
# enable "trust on first use" for host key checking
- ssh_config:
    user: root
    option: StrictHostKeyChecking
    value: no
'''

RETURN = '''
ssh_config:
    description: dictionary containing all the ssh status data
    returned: success
    type: dictionary
    contains:
        option:
            description: option to set
            returned: success
            type: string
            sample: StrictHostKeyChecking
        value:
            description: value to set
            returned: success
            type: string
            sample: no
'''

# import modules
import fileinput
import pwd
import os

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class SshConfigClient:
    configFile = None

    def __init__(self, user = None):
        if user is None:
            self.configFile = '/etc/ssh/ssh_config'
        else:
            try:
                userInfo = pwd.getpwnam(user)
            except KeyError:
                raise KeyError()

            configPath = '%s/.ssh' % (userInfo.pw_dir)

            if not os.path.isdir(configPath):
                if os.path.exists(configPath):
                    raise OSError(errno = errno.EEXIST)

                os.mkdir(configPath)
                os.chown(configPath, userInfo.pw_uid, userInfo.pw_gid)
                os.chmod(configPath, 0700)

            self.configFile = '%s/config' % (configPath)

            if not os.path.isfile(self.configFile):
                open(self.configFile, 'a').close()
                os.chown(self.configFile, userInfo.pw_uid, userInfo.pw_gid)
                os.chmod(self.configFile, 0600)

    def hasOption(self, option, value):
        config = '%s %s' % (option, value)
        isAvailable = False
        with open(self.configFile, 'r') as fd:
            if any(config in line.rstrip('\r\n') for line in fd):
                isAvailable = True

        return isAvailable

    def writeOption(self, option, value):
        for line in fileinput.input(self.configFile, inplace = True):
            if option not in line.split():
                print(line.rstrip('\r\n'))

        with open(self.configFile, 'a') as fd:
            fd.write('%s %s\n' % (option, value))

        return True

class AnsibleWrapper:
    args = None
    module = None
    ssh = None

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec = dict(
                user = dict(type = 'str'),
                option = dict(required = True, type = 'str'),
                value = dict(required = True, type = 'str')
            ),
            supports_check_mode=False
        )

        self.args = {
            'user': self.module.params.get('user'),
            'option': self.module.params.get('option'),
            'value': self.module.params.get('value')
        }

        try:
            self.ssh = SshConfigClient(self.args['user'])
        except KeyError:
            self.module.fail_json(
                msg = 'missing user (%s)' % (self.args['user'])
            )
        except OSError:
            self.module.fail_json(
                msg = 'no valid home directory for user (%s)' % (self.args['user'])
            )

    def run(self):
        if self.ssh.hasOption(self.args['option'], self.args['value']):
            self.module.exit_json(
                changed = False,
                ssh_config = {
                    'option': self.args['option'],
                    'value': self.args['value']
                }
            )
        elif self.ssh.writeOption(self.args['option'], self.args['value']):
            self.module.exit_json(
                changed = True,
                ssh_config = {
                    'option': self.args['option'],
                    'value': self.args['value']
                }
            )
        else:
            self.module.fail_json(
                msg = 'could not write config'
            )

if __name__ == '__main__':
    AnsibleWrapper().run()
