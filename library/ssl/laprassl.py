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
        required: False
        default: null
    file:
        description:
            - location at filesystem of the certificates/key
        required: False
        default: null
requirements:
    - 'python >= 2.6 # OS package'
'''

EXAMPLES = '''
# create a certificate for the inventory host
- laprassl:
    crt: "/etc/ssl/{{ inventory_hostname }}.crt.pem"
    key: "/etc/ssl/{{ inventory_hostname }}.key.pem"
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

from cryptography import x509
from cryptography.hazmat.backends import default_backend
import datetime

# import module snippets
from ansible.module_utils.basic import AnsibleModule

class LaprasslClient:
    args = None

    def __init__(self, args):
        self.args = args

    def ca(self, crt):
        payload = {
            'crt': crt
        }

        json = requests.post('%s/v1/x509/ca' % self.args['url'], data = payload).json()

        ca = ""
        for result in json['ca']:
            ca = ca + result

        return ca

    def crt(self, csr):
        payload = {
            'authkey': self.args['authkey'],
            'profile': self.args['profile'],
            'csr': csr
        }

        json = requests.post('%s/v1/x509/crt' % self.args['url'], data = payload).json()

        return json['crt']

    def csr(self, key):
        payload = {
            'cn': '', 'o': [], 'ou': [], 'st': [], 'l': [], 'c': [],
            'key': key
        }
        subject = self.args['subject'].split(", ")

        for v in subject:
            s = v.split('=')
            if s[0].lower() == 'cn':
                payload['cn'] = s[1]
            else:
                payload[s[0].lower()].append(s[1])

        json = requests.post('%s/v1/x509/csr' % self.args['url'], data = payload).json()

        return json['csr']

    def key(self):
        if self.args['keytype'] == "ec":
            payload = { 'keytype': 'ec' }
        elif self.args['keytype'] == "rsa":
            payload = { 'keytype': 'rsa', 'keysize': self.args['keysize'] }

        json = requests.post('%s/v1/key' % self.args['url'], data = payload).json()

        return json['key']

    def requireRenewal(self, path, lifetime):
        with open(path, 'rb') as fh:
            crt = fh.read()

        data = x509.load_pem_x509_certificate(crt, default_backend())
        date = data.not_valid_after - datetime.timedelta(days = lifetime)

        if datetime.datetime.now() <= date:
            return False
        else:
            return True

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
                keysize = dict(required = False, default = 4096, type = 'int'),
                authkey = dict(required = False, type = 'str'),
                subject = dict(required = False, type = 'str'),
                profile = dict(required = False, type = 'str'),
                url = dict(required = False, type = 'str'),
                file = dict(required = False, type = 'str'),
                lifetime = dict(required = False, default = 5, type = 'int')
            ),
            add_file_common_args = True,
            supports_check_mode = False
        )

        self.args = {
            'ca': self.module.params.get('ca'),
            'crt': self.module.params.get('crt'),
            'key': self.module.params.get('key'),
            'keytype': self.module.params.get('keytype'),
            'keysize': self.module.params.get('keysize'),
            'authkey': self.module.params.get('authkey'),
            'subject': self.module.params.get('subject'),
            'profile': self.module.params.get('profile'),
            'url': self.module.params.get('url'),
            'file': self.module.params.get('file'),
            'lifetime': self.module.params.get('lifetime')
        }

        self.laprassl = LaprasslClient(self.args)

    def create_ca(self):
        changed = False
        if not os.path.exists(self.args['ca']):
            with open(self.args['crt'], 'r') as fh:
                crtfile = fh.read()

            ca = self.laprassl.ca(crtfile)
            self.write(self.args['ca'], ca)
            changed = True

        return changed

    def create_crt(self):
        changed = False

        if not os.path.exists(self.args['crt']):
            if self.args['url'] != None:
                keyfile = self.read(self.args['key'])
                csr = self.laprassl.csr(keyfile)
                crt = self.laprassl.crt(csr)
            elif os.path.exists(self.args['file']):
                crt = self.read(self.args['file'])

            if crt != None:
                self.write(self.args['crt'], crt)
                changed = True
        elif self.args['url'] != None:
            if self.laprassl.requireRenewal(self.args['crt'], self.args['lifetime']) and self.create_key(True):
                keyfile = self.read(self.args['key'])
                csr = self.laprassl.csr(keyfile)
                crt = self.laprassl.crt(csr)
                self.write(self.args.crt, crt)
                changed = True

        return changed

    def create_key(self, renew = False):
        changed = False

        if not os.path.exists(self.args['key']) or renew == True:
            if self.args['url']:
                key = self.laprassl.key()
            elif os.path.exists(self.args['file']):
                key = self.read(self.args['file'])

            if key != None:
                self.write(self.args['key'], key)
                changed = True

        return changed

    def read(self, path):
        try:
            with open(path, 'r') as fh:
                content = fh.read()
        except IOError as e:
            self.module.fail_json(msg = 'failed to read file %s' % (e))

        return content

    def write(self, path, content):
        try:
            with open(path, 'w') as fh:
                fh.write(content)
        except IOError as e:
            self.module.fail_json(msg = 'failed to create file: %s' % (e))

    def run(self):
        if self.args['key'] != None:
            changed = self.create_key()
            params = self.module.params
            params['path'] = self.args['key']
            file_args = self.module.load_file_common_arguments(params)
            file_args['path'] = self.args['key']
            self.changed = self.module.set_fs_attributes_if_different(file_args, changed)

        if self.args['crt'] != None:
            changed = self.create_crt()
            params = self.module.params
            params['path'] = self.args['crt']
            file_args = self.module.load_file_common_arguments(params)
            file_args['path'] = self.args['crt']
            self.changed = self.module.set_fs_attributes_if_different(file_args, changed)

        if self.args['ca'] != None and self.args['crt'] != None:
            changed = self.create_ca()
            params = self.module.params
            params['path'] = self.args['ca']
            file_args = self.module.load_file_common_arguments(params)
            file_args['path'] = self.args['ca']
            self.changed = self.module.set_fs_attributes_if_different(file_args, changed)

        self.module.exit_json(
            changed = self.changed
        )

if __name__ == '__main__':
    AnsibleWrapper().run()
