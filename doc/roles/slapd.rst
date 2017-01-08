slapd
=====

description
  LDAP suite of application and development tools

website
  http://www.openldap.org

license
  OPENLDAP GPL-2

dependencies
------------

- common

variables
---------

.. code-block:: json
   'slapdConfig' {
    'db': {
      'mdb': {
        // required: yes
        // description: domain name
        'suffix': 'dc=example,dc=org',

        // required: yes
        // description: password of the root db user
        'password': '<string>'
      },
      'config': {
        // required: yes
        // description: password of the config root user
        'password': '<string>'
      }
    }
   }
