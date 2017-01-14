rabbitmq
========

description
  RabbitMQ is a high-performance AMQP-compliant message broker written in Erlang

website
  http://www.rabbitmq.com/

license
  GPL-2

dependencies
------------

- common
- nginx

variables
---------

.. code-block:: json
   'rabbitmqConfig' {
    // required: yes
    // description: node name
    'name': '<string>',
    // required: yes
    // description: password of default user
    'password': '<string>'
    // required: no
    // description: list of virtual hosts
    'vhosts': {
      '<string>': {
        'user': [
          {
            // required: yes
            // description: name of user
            'username': '<string>',
            // required: yes
            // description: password of user
            'password': '<string>'
          }
        ]
      }
    }
   }
