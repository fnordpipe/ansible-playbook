#!/usr/bin/python

# Copyright (c) 2017 crito <crito@fnordpipe.org>

DOCUMENTATION = '''
---
module: laprassl
short_description: manage x509 certificates
description:
    - creates or updates x509 certificates
options:
    crt:
        description:
            - path to certificate
        required: True
        default: null
    key:
        description:
            - path to key file
        required: True
        default: null
    keytype:
        description:
            - type of key e.g. ec, rsa
        required: False
        default: ec
    keysize:
        description:
            - size of the key. Optional for keytype rsa
        required: False
        default: 4096
    authkey:
        description:
            - authentication key to create certificates
        required: True
        default: null
    subject:
        description:
            - name of the certificate
        required: True
        default: null
    profile:
        description:
            - profile of the to generating certificate
        required: True
        default: null
    url:
        description:
            - url of the laprassl server
        required: True
        default: null
requirements:
    - 'python >= 2.6 # OS package'
'''

EXAMPLES = '''
# create a certificate for the inventory host
- laprassl:
    crt: "/etc/ssl/{{ inventory_hostname}}.crt.pem"
    key: "/etc/ssl/{{ inventory_hostname}}.key.pem"
    authkey: changeme
    subject: CN=example.org O=example org O=example organization
    profile: server
    url: https://127.0.0.1
'''

RETURN = '''
laprassl:
    description: dictionary containing metadata of certificate
    returned: success
    type: dictionary
    contains:
        valid_to:
            description: validation timestamp
            returned: success
            type: number
            sample: 1488574167
        valid_from:
            description: validation timestamp
            returned: success
            type: number
            sample: 1488574167
        subject:
            description: subject of the certificate
            returned: success
            type: string
            sample: CN=example.org O=example
'''

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class AnsibleWrapper:
    args = None
    module = None
    userInfo = None

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec = dict(
                crt = dict(required = True, type = 'str'),
                key = dict(required = True, type = 'str'),
                keytype = dict(required = True, type = 'str'),
                keysize = dict(required = True, type = 'int'),
                authkey = dict(required = True, type = 'str'),
                subject = dict(required = True, type = 'str'),
                profile = dict(required = True, type = 'str'),
                url = dict(required = True, type = 'str'),
            ),
            supports_check_mode = False
        )

        self.args = {
            'crt': self.module.params.get('crt'),
            'key': self.module.params.get('key'),
            'keytype': self.module.params.get('keytype'),
            'keysize': self.module.params.get('keysize'),
            'authkey': self.module.params.get('authkey'),
            'subject': self.module.params.get('subject'),
            'profile': self.module.params.get('profile'),
            'url': self.module.params.get('url')
        }

    def run(self):
        self.module.exit_json(
            changed = False,
            laprassl = {
                'valid_to': self.laprassl['valid_to']
                'valid_from': self.laprassl['valid_from']
                'valid_subject': self.laprassl['valid_subject']
            }
        )

if __name__ == '__main__':
    AnsibleWrapper().run()
