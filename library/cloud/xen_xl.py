#!/usr/bin/python

# Copyright (c) 2016 crito <crito@fnordpipe.org>

DOCUMENTATION = '''
---
module: xen_xl
short_description: manage domU's
description:
    - manage domU's
options:
    name:
        description:
            - name of the dom'U
        required: True
        default: null
    config:
        description:
            - The full path of the config file
        required: True
        default: null
    state:
        description:
            - Check's whether machine is in state 'started', 'stopped', 'present' or 'absent'
        required: False
        default: started
    template:
        description:
            - name of the template to use within a xen create
        required: False
        default: gentoo-overlay
    template_args:
        description:
            - additional arguments for the domU install template
        required: False
        default: null
requirements:
    - 'python >= 2.6 # OS package'
'''

EXAMPLES = '''
# Create a started dom'U
- xen_xl:
    config: /etc/xen/config/example.conf
    state: started
    name: example
    template: gentoo-overlay
'''

RETURN = '''
xen_xl:
    description: dictionary containing all the xen status data
    returned: success
    type: dictionary
    contains:
        name:
            description: name of the dom'U
            returned: success
            type: string
            sample: example
        state:
            description: resulting state of the dom'U
            returned: success
            type: string
            sample: "started"
'''

# import modules
import subprocess
import os
import imp

from shutil import copyfile

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class XenXlClient:
    name = None
    config = None
    state = None
    template = None

    def __init__(self, name, config, template):
        self.name = name
        self.config = { 'template': config, 'file': '/var/lib/xen/%s/config' % (name) }
        self.state = self.getXlState()
        self.template = template

    def createXl(self):
        xl = subprocess.Popen(
            ['xl', 'create', self.config['file']],
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        stdOut, stdErr = xl.communicate()
        self.state = self.getXlState()

        if xl.returncode == 0:
            return True
        else:
            return False

    def destroyXl(self):
        xl = subprocess.Popen(
            ['xl', 'destroy', self.name],
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        stdOut, stdErr = xl.communicate()
        self.state = self.getXlState()

        if xl.returncode == 0:
            return True
        else:
            return False

    def getState(self):
        return self.state

    def getXlState(self):
        xl = subprocess.Popen(
            ['xl', 'list', self.name],
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        stdOut, stdErr = xl.communicate()

        if xl.returncode == 0:
            mode = stdOut.split('\n')[1].split()[4]
            if mode.find('r') > -1 or mode.find('b') > -1:
                state = 'started'
            elif mode.find('s') > -1:
                state = 'stopped'
            else:
                state = 'present'
        elif os.path.isfile(self.config['file']):
            state = 'present'
        else:
            state = 'absent'

        return state

    def hasState(self, state):
        if state == self.state or (state == 'present' and self.state in ['started', 'stopped', 'present']):
            return True
        else:
            return False

    def installXl(self, args = None):
        fd = open(self.config['template'])
        lvmDev = imp.load_source('xlConfig', '', fd).disk[0].split(',')[0][4:]
        fd.close()
        templateArgs = args.split(' ') if args is not None else []

        xl = subprocess.Popen(
            ['/usr/share/xen/templates/xen-%s' % (self.template), '--hostname=%s' % (self.name), '--dev=%s' % (lvmDev)] + templateArgs,
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        stdOut, stdErr = xl.communicate()

        if xl.returncode == 0:
            if not os.path.exists('/var/lib/xen/%s' % (self.name)):
                os.mkdir('/var/lib/xen/%s' % (self.name), 0750)

            copyfile(self.config['template'], self.config['file'])
            self.state = self.getXlState()
            return True
        else:
            return False

    def removeXl(self):
        if os.path.exists(self.config['file']):
            os.remove(self.config['file'])
        self.state = self.getXlState()

    def shutdownXl(self):
        xl = subprocess.Popen(
            ['xl', 'shutdown', self.name],
            stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE
        )
        stdOut, stdErr = xl.communicate()

        # dear future self, please fix this
        i = 0
        while self.state != 'stopped':
            self.state = self.getXlState()
            ++i

            if i == 9:
                break;

        if xl.returncode == 0:
            return True
        else:
            return False

class AnsibleWrapper:
    args = None
    module = None
    xl = None

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec = dict(
                config = dict(required = True, type = 'path'),
                state = dict(type = 'str', default = 'started'),
                name = dict(required = True, type = 'str'),
                template = dict(type = 'str', default = 'gentoo-overlay'),
                template_args = dict(type = 'str')
            ),
            supports_check_mode = False
        )

        self.args = {
            'name': self.module.params.get('name'),
            'config': self.module.params.get('config'),
            'state': self.module.params.get('state'),
            'template': self.module.params.get('template'),
            'templateArgs': self.module.params.get('template_args')
        }

        self.xl = XenXlClient(self.args['name'], self.args['config'], self.args['template'])

    def doCreate(self):
        if not self.xl.installXl(self.args['templateArgs']):
            self.module.fail_json(
                msg = 'failed to install template %s' % (self.args['template'])
            )

        if self.xl.hasState(self.args['state']):
            self.module.exit_json(
                changed = True,
                xen_xl = {
                    'name': self.args['name'],
                    'state': self.xl.getState()
                }
            )
        else:
            self.module.fail_json(
                msg = 'failed to set state %s, current state is %s' % (self.args['state'], self.xl.getState())
            )

    def doRemove(self):
        self.xl.destroyXl()
        self.xl.removeXl()

        if self.xl.hasState(self.args['state']):
            self.module.exit_json(
                changed = True,
                xen_xl = {
                    'name': self.args['name'],
                    'state': self.xl.getState()
                }
            )
        else:
            self.module.fail_json(
                msg = 'failed to set state %s, current state is %s' % (self.args['state'], self.xl.getState())
            )


    def doStart(self):
        if self.xl.getState() in ['stopped', 'present']:
            self.xl.destroyXl()

        if self.xl.getState() == 'absent':
            if not self.xl.installXl(self.args['templateArgs']):
                self.module.fail_json(
                    msg = 'failed to install template %s' % (self.args['template'])
                )

        self.xl.createXl()

        if self.xl.hasState(self.args['state']):
            self.module.exit_json(
                changed = True,
                xen_xl = {
                    'name': self.args['name'],
                    'state': self.xl.getState()
                }
            )
        else:
            self.module.fail_json(
                msg = 'failed to set state %s, current state is %s' % (self.args['state'], self.xl.getState())
            )

    def doStop(self):
        if self.xl.getState() == 'present':
            self.xl.destroyXl()
            self.xl.createXl()

        if self.xl.getState() == 'absent':
            if self.xl.installXl():
                self.xl.createXl()
            else:
                self.module.fail_json(
                    msg = 'failed to install template %s' % (self.args['template'])
                )

        if self.xl.getState() == 'started':
            self.xl.shutdownXl()

        if self.xl.hasState(self.args['state']):
            self.module.exit_json(
                changed = True,
                xen_xl = {
                    'name': self.args['name'],
                    'state': self.xl.getState()
                }
            )
        else:
            self.module.fail_json(
                msg = 'failed to set state %s, current state is %s' % (self.args['state'], self.xl.getState())
            )

    def run(self):
        if self.xl.hasState(self.args['state']):
            self.module.exit_json(
                changed = False,
                xen_xl = {
                    'name': self.args['name'],
                    'state': self.args['state']
                }
            )

        if self.args['state'] == 'started':
            self.doStart()

        if self.args['state'] == 'stopped':
            self.doStop()

        if self.args['state'] == 'present':
            self.doCreate()

        if self.args['state'] == 'absent':
            self.doRemove()

if __name__ == '__main__':
    AnsibleWrapper().run()
