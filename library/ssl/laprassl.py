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
        required: False
        default: null
    key:
        description:
            - path to key file
        required: False
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
    subject: "CN=example.org, O=example org, O=example organization"
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

# import module
import os.path
import requests

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class LaprasslClient:
    args = None

    def __init__(self, args):
        self.args = args

    def crt(self, csr):
        payload = {
            'authkey': self.args.authkey,
            'profile': self.args.profile,
            'csr': csr
        }

        json = requests.post('%s/v1/crt' % self.args.url, data = payload).json

        return json['crt']

    def csr(self, key):
        payload = {
            'cn': '', o = [], ou = [], st = [], l = [], c = [],
            'key' key
        }
        subject = self.args.subject.split(', ')

        for k, v in subject:
            s = v.split('=')
            if s[0] == 'cn':
                payload['cn'] = s[1]
            else
                payload[s[0]].append(s[1])

        json = requests.post('%s/v1/csr' % self.args.url, data = payload).json()

        return json['csr']

    def key(self):
        if self.args.keytype == "ec":
            payload = { 'keytype': 'ec' }
        else if self.args.keytype == "rsa":
            payload = { 'keytype': 'rsa', 'keysize': self.args.keysize }

        json = requests.post('%s/v1/key' % self.args.url, data = payload).json()

        return json['key']

class AnsibleWrapper:
    args = None
    module = None
    laprassl = None
    changed = None

    def __init__(self):
        self.module = AnsibleModule(
            argument_spec = dict(
                crt = dict(required = False, type = 'path'),
                key = dict(required = False, type = 'path'),
                ca = dict(required = False, type = 'path'),
                keytype = dict(required = False, default = 'ec', type = 'str'),
                keysize = dict(required = False, default = 4096 type = 'int'),
                authkey = dict(required = True, type = 'str'),
                subject = dict(required = True, type = 'str'),
                profile = dict(required = True, type = 'str'),
                url = dict(required = True, type = 'str'),
                lifetime = dict(required = False, default = 5, type = 'str')
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
            'url': self.module.params.get('url'),
            'lifetime': self.module.params.get('lifetime')
        }

        self.laprassl = LaprasslClient(self.args)

    def create_crt(self, key):
        if not os.path.exists(self.args.crt):
            csr = self.laprassl.csr(key)
            crt = self.laprassl.crt(csr)
            self.write(self.args.crt, crt)
            self.changed = True
        else
            with open(self.args.crt, 'r') as fh:
                content = fh.read()

            if self.laprassl.getLifetime(content) < self.args.lifetime:
                csr = self.laprassl.csr(key)
                crt = self.laprassl.crt(csr)
                self.write(self.args.crt, crt)
                self.changed = True

    def create_key(self):
        if not os.path.exists(self.args.key):
            key = self.laprassl.key()
            self.write(self.args.key, key)
            changed = True
        else:
            changed = False

        return changed

    def write(self, path, content):
        try:
            with open(path, 'w') as fh:
                fh.write(content)
        except IOError e:
            self.module.fail_json(msg = 'failed to create file: %s' % (e))

    def run(self):
        if self.args.key != None:
            changed = self.create_key()
            file_args = self.module.load_common_arguments(self.module.params)
            file_args['path'] = self.args.key
            self.changed = self.module.set_fs_attributes_if_different(file_args, changed)

        if self.args.crt != None:
            changed = self.create_crt(key)
            file_args = self.module.load_common_arguments(self.module.params)
            file_args['path'] = self.args.crt
            self.changed = self.module.set_fs_attributes_if_different(file_args, changed)

if __name__ == '__main__':
    AnsibleWrapper().run()
