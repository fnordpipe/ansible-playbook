dom0
====

description
  The Xen virtual machine monitor

website
  http://xen.org/

license
  GPL-2

dependencies
------------

- common

groups
------

dom0-<fqdn>
  list of domU's assigned to this dom0

variables
---------

.. code-block:: json
   'dom0Config': {
    // required: no
    // description: prefix for mac addresses of virtual machines
    'macprefix': 'de:ad:be:ef'
   }

requires
--------

.. code-block:: json
   // config of assigned domU
   'commonConfig': {
    'network': {
      // required: no
      // description: default interface
      'default': 'eth0'
    }
   }

.. code-block:: json
   // config of assigned domU
   'domUConfig': {
    // required: no
    // description: default bridge
    'bridge': 'br0'
   }

.. code-block:: json
   // config of assigned domU
   'dom0Config': {
    // required: no
    // description: bridge device where domU is assigned to
    'bridge': 'br0',
    // required: no
    // description: kernel to boot in domU
    'kernel': '/boot/kernel',
    // required: no
    // description: size of logical volume
    'lvSize': '10g',
    // required: no
    // description: amount of memory of domU
    'memory': '4096',
    // required: yes
    // description: installer for domU image
    'template': 'yourInstallTemplate',
    // required: no
    // description: amount of vcpus of domU
    'vcpus': '4'
   }
