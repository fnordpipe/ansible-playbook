phpmyadmin
==========

description
  Web-based administration for MySQL database in PHP

website
  https://www.phpmyadmin.net/

license
  GPL-2

dependencies
------------

- common
- php

variables
---------

.. code-block:: json
   'phpmyadminConfig' {
    // required: yes
    // description: random token for blowfish crypto
    'blowfish': '<string>',
    // required: yes
    // description: mysql hoststring
    'host': '<string>',
   }
