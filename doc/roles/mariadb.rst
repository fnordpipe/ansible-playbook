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
    'user': {
      'root': {
        // required: yes
        // description: password for root user
        'password': '<string>'
      }
    }
   }
