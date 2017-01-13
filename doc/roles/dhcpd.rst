dhcpd
=====

description
  ISC Dynamic Host Configuration Protocol (DHCP) server

website
  http://www.isc.org/products/DHCP

license
  ISC

dependencies
------------

- common

groups
------

all
  all hosts will be written to dhcp host config
  to assign a static ip

variables
---------

.. code-block:: json
   'dhcpdConfig': {
    // required: yes
    // description: rdnc key for dynamic dns updates
    'ddns-key': '<string>',
    // required: yes
    // description: interface to listen on
    'interface': 'eth0',
    'cache': {
      // required: yess
      // description: db of ansible cache server
      'db': '0',
      // required: yes
      // description: hostname of ansible cache server
      'host': 'cache.example.org',
      // required: yes
      // description: password of ansible cache server
      'password': 'examplePassword',
      // required: yes
      // description: port of ansible cache server
      'port': '1234'
    },
    // required: no
    // description: default route
    'defaultRoute': '10.255.255.1',
    // required: no
    // description: list of addresses of dns servers
    'dnsServers': '85.214.20.141',
    // required: no
    // description: domain name of network zone
    'domainName': 'example.org',
    // required: no
    // description: leasetime of address
    'lease': '86400',
    // required: no
    // description: netmask of managed net
    'netmask': '255.255.255.0',
    // required: no
    // description: end of range of managed ip addresses
    'rangeEnd': '10.255.255.254',
    // required: no
    // description: start of range of managed ip addresses
    'rangeStart': '10.255.255.20',
    // required: no
    // description: subnet id of managed net
    'subnetId': '10.255.255.0'
   }
