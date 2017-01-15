phppgadmin
==========

description
  Web-based administration for Postgres database in php

website
  http://phppgadmin.sourceforge.net/

license
  GPL-2

dependencies
------------

- common
- php

variables
---------

.. code-block:: json
   'phppgadminConfig' {
    // required: yes
    // description: description of server
    'desc': '<string>',
    // required: yes
    // description: postgres hoststring
    'host': '<string>',
   }
