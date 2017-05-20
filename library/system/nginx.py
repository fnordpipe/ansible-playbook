#!/usr/bin/python

# Copyright (c) 2017 crito <crito@fnordpipe.org>

DOCUMENTATION = '''
---
module: nginx
short_description: manage x509 certificate for nginx
description:
    - creates or updates x509 certificates for nginx
options:
    crt:
        description:
            - path to certificate
        required: True
        default: null
    ca:
        description:
            - path to ca file
        required: True
        default: null
    dest:
        description:
            - destination of nginx certificate file
        required: True
        default: null
requirements:
    - 'python >= 2.6 # OS package'
'''

EXAMPLES = '''
# create a certificate for the inventory host
- laprassl:
    crt: "/etc/ssl/{{ inventory_hostname }}.crt.pem"
    ca: "/etc/ssl/rootca.crt.pem"
    dest; "/etc/ssl/{{ inventory_hostname }}.nginx.pem"
'''

RETURN = '''
nginx:
    description: dictionary containing info about task
    returned: success
    type: dictionary
    contains:
        changed:
            description: state of modification of nginx certificate
            returned: success
            type: number
            sample: True
'''

# import module
import os.path

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class AnsibleWrapper:
    args = None
    module = None
    changed = None

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec = dict(
                crt = dict(required = True, type = 'path'),
                ca = dict(required = True, type = 'path'),
                dest = dict(required = True, type = 'path'),
            ),
            add_file_common_args = True,
            supports_check_mode = False
        )
        self.args = {
            'crt': self.module.params.get('crt'),
            'ca': self.module.params.get('ca'),
            'dest': self.module.params.get('dest')
        }
        self.changed = False

    def run(self):
      if os.path.exists(self.args['crt']) and os.path.exists(self.args['ca']):
        try:
          with open(self.args['crt'], 'r') as fh:
            crt = fh.read()
          with open(self.args['ca'], 'r') as fh:
            ca = fh.read()
          if os.path.exists(self.args['dest']):
            with open(self.args['dest'], 'r') as fh:
              nginx = fh.read()
        except IOError as e:
          self.module.fail_json(msg = 'failed to read file %s' % e)

        dest = crt + ca

        if nginx != dest:
          try:
            with open(self.args['dest'], 'w') as fh:
              fh.write(dest)

            self.changed = True
          except IOError as e:
            self.module.fail_json(msg = 'failed to read file %s' % e)

        params = self.module.params
        params['path'] = self.args['dest']
        file_args = self.module.load_file_common_arguments(params)
        file_args['path'] = self.args['dest']
        self.changed = self.module.set_fs_attributes_if_different(file_args, self.changed)

        self.module.exit_json(
            changed = self.changed
        )

if __name__ == '__main__':
    AnsibleWrapper().run()
