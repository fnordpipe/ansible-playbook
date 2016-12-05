common
======

description
  role independent configurations

variables
---------

.. code-block:: json
   'commonConfig' {
    'gentoo': {
      // required: no
      // description: set the default repo
      'main-repo': 'gentoo',
      // required: no
      // description: set the system profile
      'profile': '/usr/local/example-overlay/profiles/your/profile',
      'repos': [
        {
          // required: no
          // description: location of your portage tree
          'location': '/usr/local/example',
          // required: no
          // description: set name of your custom gentoo overlay
          'name': 'example',
          // required: no
          // description: type of your portage mirrors
          'sync-type': 'rsync',
          // required: no
          // description: uri of your portage mirror
          'sync-uri': 'rsync://rsync.example.org/portage'
        }
      ]
    },
    'network': {
      // required: no
      // description: define default gw interface
      'default': 'br0',
      'interfaces': {
        'br0': {
          // required: no
          // description: interfaces bind to this bridge
          'bridge': 'eth0',
          // required: no
          // description: address of the target host (ip || dhcp || null)
          'ipv4addr': '10.0.0.100',
          // required: no
          // description: set default route for target host
          'ipv4route': '10.0.0.1',
          // required: no
          // description: subnet of the target host
          'subnet': '/24'
        }
      },
      // required: no
      // description: set's default dns server
      'nsServer': [
        '10.0.0.2'
      ]
    },
    // required: yes
    // description: ssh public key to write to authorized_keys file
    'sshPubKey': '<type> <key> <comment>'
   }
