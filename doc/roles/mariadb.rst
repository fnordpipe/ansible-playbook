mariadb
=======

description
  An enhanced, drop-in replacement for MySQL

website
  http://mariadb.org/

license
  GPL-2

dependencies
------------

- common

variables
---------

.. code-block:: json
   'mariadbConfig' {
    // required: yes
    // description: password of root user
    'password': '<string>',
    'user': {
      '<string>': {
        // required: no
        // description: host part of mariadb user
        'host': '<string>',
        // required: yes
        // description: password of user
        'password': '<string>'
      }
    }
   }
