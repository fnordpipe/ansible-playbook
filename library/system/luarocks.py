#!/usr/bin/env python
# vim:fileencoding=utf-8

"""
(c) 2014, Mario César Señoranis Ayala <mariocesar.c50@gmail.com>
TODO:
    - Enforce version
    - Support for --local argument
    - Support build parameters
"""

# TODO:

DOCUMENTATION = '''
---
module: luarocks
short_description: Manage lua modules with luarocks (http://luarocks.org)
description:
  - Manage lua packages with luarocks (http://luarocks.org)
version_added: 1.9
author: "Mario César Señoranis Ayala (@humanzilla)"
options:
  name:
    description:
      - The name of the lua module
    required: true
  state:
    description:
      - The state of the lua module
    required: false
    default: present
    choices: [ "present", "absent" ]
'''

EXAMPLES = '''
description: Install "md5" lua module.
- luarocks: name=md5
description: Remove the "md5" lua module.
- luarocks: name=md5 state=absent
'''

import re
from ansible.module_utils.basic import *


class Luarock(object):
    def __init__(self, module, name, state):
        self.name = name
        self.state = state
        self.module = module

    def _exec(self, args, run_in_check_mode=False, check_rc=True):
        if not self.module.check_mode or (self.module.check_mode and run_in_check_mode):
            cmd = ["luarocks"] + args
            rc, out, err = self.module.run_command(cmd, check_rc=check_rc)

            if err:
                self._fail(err, rc)

            return out
        return ''

    def _fail(self, err, rc):
        self.module.fail_json(
            name=self.name, state=self.tag, msg=err, rc=rc
        )

    def list(self):
        """Returns a list of installed modules"""
        out = self._exec(['list'])
        catalogue = re.findall('([\w\-]+)\n   (.+) \((.+)\)', out, re.MULTILINE)
        return [dict(zip(('name', 'version', 'status'), item)) for item in catalogue]

    def installed(self):
        """Test module name is installed"""
        if any([item['name'] == self.name for item in self.list()]):
            return True
        return False

    def install(self):
        if not self.installed():
            return self._exec(['install', self.name])

    def remove(self):
        if self.installed():
            return self._exec(['remove', self.name])


def main():
    module = AnsibleModule(
        argument_spec = dict(
            name      = dict(required=True),
            state     = dict(default='present', choices=['present', 'absent']),
        )
    )

    name = module.params['name']
    state = module.params['state']

    if module.check_mode:
        module.exit_json(changed=False)

    luarocks = Luarock(module=module, name=name, state=state)

    changed = False
    if state == 'present' and luarocks.install():
        changed = True
    elif state == 'absent' and luarocks.remove():
        changed = True

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
