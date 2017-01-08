nginx
=====

description
  Robust, small and high performance http and reverse proxy server

website
  http://nginx.org

license
  BSD MIT GPL-2

dependencies
------------

- common

variables
---------

.. code-block:: json
   'nginxConfig' {
    // required: no
    // description: profiles of nginx instance
    'profiles': {
      'dirlisting': {
        'sshPubKeys': [
          // required: no
          // description: ssh public key for authorized_keys of dirlisting user
          '<string>'
        ]
      }
    },
    // required: no
    // description: amount of connections per worker
    'worker_connections': '1024',
    // required: no
    // description: amount of worker processes
    'worker_processes': '2'
   }
