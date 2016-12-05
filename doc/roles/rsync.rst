rsync
=====

description
  File transfer program to keep remote files into sync

website
  http://rsync.samba.org/

license
  GPL-3

dependencies
------------

- common

variables
---------

.. code-block:: json
   'rsyncConfig' {
    'repos': [
      {
        // required: yes
        // description: description of rsync repo
        'description': 'lorem ipsum dolor sit amet',
        // required: yes
        // description: name of rsync repo
        'name': 'foo'
      }
    ],
    'sshPubKeys': [
      // required: yes
      // description: ssh public key for authorized_keys
      'ssh-ed25519 dsnebadfbedas93843 user@example.org'
    ]
   }
