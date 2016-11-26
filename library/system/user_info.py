#!/usr/bin/python

# Copyright (c) 2016 crito <crito@fnordpipe.org>

DOCUMENTATION = '''
---
module: user_info
short_description: prints user info
description:
    - prints user info from /etc/passwd
options:
    user:
        description:
            - name of the user
        required: True
        default: null
requirements:
    - 'python >= 2.6 # OS package'
'''

EXAMPLES = '''
# read user foo's home dir
- user_info:
    user: foo
  register: fooVar

- debug:
    msg: "{{ fooVar.home }}"
'''

RETURN = '''
user_info:
    description: dictionary containing all the user data
    returned: success
    type: dictionary
    contains:
        home:
            description: home dir of user
            returned: success
            type: string
            sample: /home/foo
'''

# import modules
import pwd

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class AnsibleWrapper:
    args = None
    module = None
    userInfo = None

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec = dict(
                user = dict(required = True, type = 'str')
            ),
            supports_check_mode = False
        )

        self.args = {
            'user': self.module.params.get('user')
        }

        try:
            self.userInfo = {
                'home': pwd.getpwnam(self.args['user']).pw_dir
            }
        except KeyError:
            self.module.fail_json(
                msg = 'user (%s) not found' % (self.args['user'])
            )

    def run(self):
        self.module.exit_json(
            changed = False,
            user_info = {
                'home': self.userInfo['home']
            }
        )

if __name__ == '__main__':
    AnsibleWrapper().run()
