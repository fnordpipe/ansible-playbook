phpldapadmin
============

description
  phpLDAPadmin is a web-based tool for managing all aspects of your LDAP server

website
  http://phpldapadmin.sourceforge.net

license
  GPL-2

dependencies
------------

- common
- php

variables
---------

.. code-block:: json
   'phpldapadminConfig' {
    // required: yes
    // description: random token for blowfish crypto
    'blowfish': '<string>',
    // required: yes
    // description: ldap hoststring e.g. ldap://ldap.example.org
    'host': '<string>',
    // required: yes
    // description: name of ldap server
    'name': '<string>',
    // required: yes
    // description: port of ldap server
    'port': '<int>'
   }
