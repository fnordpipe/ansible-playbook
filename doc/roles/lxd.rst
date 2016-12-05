lxd
===

description
  LinuX Containers userspace utilities

website
  https://linuxcontainers.org/

license
  LGPL-3

dependencies
------------

- common

groups
------

lxd-<fqdn>
  list of hosts assigned to this lxd host

variables
---------

.. code-block:: json
   'lxdConfig' {
    // required: no
    // description: prefix of mac address of container
    'macprefix': 'de:ad:be:ef'
   }

requires
--------

.. code-block:: json
   // config of assigned linux container
   'commonConfig': {
    'network': {
      // required: no
      // description: interface name
      'default': 'eth0',
      'interfaces': {
        'eth0': {
          // required: no
          // description: ip address of container (ipaddr, dhcp, null)
          'ipv4addr': '10.255.255.123',
          // required: no
          // description: default route of container
          'ipv4route': '10.255.255.1',
          // required: no
          // description: subnet of container
          'subnet': '/24'
        }
      }
    }
   }

.. code-block:: json
   // config of assigned linux container
   'lxdConfig': {
    // required: no
    // description: bridge where the container is assigned to
    'bridge': 'br0'
   }
