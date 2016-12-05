git
===

description
  stupid content tracker: distributed VCS designed for speed and efficiency

website
  http://www.git-scm.com

license
  GPL-2

dependencies
------------

- common
- webserver

variables
---------

.. code-block:: json
   'gitConfig' {
    // required: no
    // description: description of cgit instance
    'description': 'lorem ipsum dolor sit amet',
    'repos': [
      {
        // required: yes
        // description: subdirectory of repo
        'category': 'foo',
        // required: yes
        // description: description of repo
        'description': 'lorem ipsum dolor sit amet',
        // required: yes
        // description: name of repo
        'name': 'bla',
        // required: yes
        // description: owner of repo
        'owner': 'user',
        // required: yes
        // description: section of repo
        'section': 'lorem ipsum'
      }
    ],
    'sshPubKeys': [
      // required: no
      // description: ssh pubkeys with access to all git repos
      'ssh-ed25519 dsnebadfbedas93843 user@example.org'
    ],
    // required: no
    // description: title of cgit instance
    'title': 'foo git',
   }
