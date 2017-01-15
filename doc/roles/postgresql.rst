postgresql
==========

description
  PostgreSQL RDBMS

website
  http://www.postgresql.org/

license
  POSTGRESQL GPL-2

dependencies
------------

- common

variables
---------

.. code-block:: json
   'postgresqlConfig' {
    // required: yes
    // description: password of root user
    'password': '<string>',
    // required: no
    // description: list of users and databases
    'user': [
      {
        // required: yes
        // description: name of user and database
        'name': '<string>',
        // required: yes
        // description: password of user
        'password': '<string>'
      }
    ]
   }
