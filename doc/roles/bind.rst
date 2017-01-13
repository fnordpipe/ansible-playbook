bind
====

description
  BIND - Berkeley Internet Name Domain - Name Server

website
  http://www.isc.org/software/bind

license
  ISC

dependencies
------------

- common

groups
------

all
  the dynamic zones will be created by gathering all fqdn's based on the inventory.

variables
---------

.. code-block:: json
   'bindConfig': {
    // required: yes
    // description: rdnc key for dynamic dns updates
    'ddns-key': '<string>',
    // required: yes
    // description:
    'internal': {
      // required: yes
      // description: networks for acl zone "trusted"
      'acl': [
        '10.255.255.0/24'
      ],
      'zones': {
        'example.org': [
          // required: yes
          // description: name of record
          'name': 'sub',
          // required: yes
          // description; type
          'type': 'CNAME',
          // required: yes
          // description: target of dns record
          'data': 'foo.example.org'
        ]
      }
    },
    // required: yes
    // description: name server of SoA
    'soaNs': 'ns.example.org',
    // required: yes
    // description: contact address of SoA
    'soaContact': 'soa.example.org'
   }
