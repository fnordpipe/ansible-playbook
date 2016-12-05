buildbot
========

description
  BuildBot build automation system

website
  http://trac.buildbot.net/

license
  GPL-2

dependencies
------------

- common

groups
------

buildmaster-<fqdn>
  list of slaves assigned to this buildmaster

master
------

variables
~~~~~~~~~

.. code-block:: yaml
   authConfig:
    # required: yes
    # description: private ssh key for git auth
    sshKey: |
      your
      private
      key

.. code-block:: json
   'buildbotConfig': {
    'master': {
      // required: yes
      // description: name of buildmaster instance
      'name': 'example',
      // required: yes
      // description: title of instance
      'title': 'exambot',
      // required: yes
      // description: url of te project page
      'titleUrl': 'http://sub.example.org',
      // required: yes
      // description: url of buildbot instance
      'buildbotUrl': 'http://127.0.0.1:8010.',
      'poller': [
        // required: yes
        // description: project identifier
        'project': 'yourExampleProject',
        // required: yes
        // description: url of repository
        'url': 'git@git.example.org/yourExampleProject.git',
        'branches': [
          // required: yes
          // description: name of branch to monitor
          'master'
        ],
        // required: yes
        // description: workdir of poller
        'workdir': 'yourExampleProject',
        // required: yes
        // description: interval for cvs scan (in secconds)
        'interval': '300'
      ],
      'scheduler': {
        // required: no
        // description: add nightly scheduler
        'nightly': {
          // required: yes
          // description: name of scheduler
          'name': 'yourExampleNightly',
          // required: yes
          // description: project to schedule
          'project': 'yourExampleProject',
          // required: yes
          // description: branch to schedule
          'branch': 'master',
          'builderNames': [
            // required: yes
            // description: name of builder to run
            'yourBuilder'
          ],
          // required: yes
          // description: hour of day
          'hour': '1',
          // required: yes
          // description: minute of hour
          'minute': '0'
        },
        // required: no
        // description: add change scheduler
        'change': {
          // required: yes
          // description: name of scheduler
          'name': 'yourExampleChange',
          // required: yes
          // description: project to schedule
          'project': 'yourExampleProject',
          // required: yes
          // description: branch to schedule
          'branch': 'master',
          'builderNames': [
            // required: yes
            // description: name of builder to run
            'yourBuilder'
          ],
          // required: yes
          // description: idle time before build is triggered
          'treeStableTimer': '300',
        },
        // required: no
        // description: add periodic scheduler
        'periodic': {
          // required: yes
          // description: name of scheduler
          'name': 'yourExampleChange',
          'builderNames': [
            // required: yes
            // description: name of builder to run
            'yourBuilder'
          ],
          // required: yes
          // description: interval of execution
          'periodicBuildTimer': '300',
        },
      },
      // required: no
      // description: factories of buildbot
      'factory': [
        // required: yes
        // description: name of factory
        'name': 'yourFactory',
        'steps': {
          'git': [
            {
              // required: yes
              // description: name of step
              'name': 'yourGitStep',
              // required: yes
              // description: url of cvs repo
              'repourl': 'git@git.example.org/yourProject.git',
              // required: no
              // description: work directory path
              'workdir': 'yourProjectWorkDir',
              // required: no
              // description: mode of checkout
              'mode': 'incremental',
              // required: no
              // description: use latest commit
              'alwaysUseLatest': 'True',
              // required: no
              // description: halt on failure
              'haltOnFailure': 'True'
            }
          ],
          'shell': [
            {
              // required: yes
              // description: name of step
              'name': 'yourShellStep',
              // required: yes
              // description: command to invoke
              'command': 'make all',
              // required: no
              // description: work directory
              'workdir': 'yourProjectWorkDir',
              // required: no
              // description: max time of execution (in seconds)
              'timeout': '1800',
              // required: no
              // description: halt on failure
              'haltOnFailure': 'True',
              // required: no
              // description: run altough previous step failes
              'alwaysRun': 'False',
              'builder': {
                // required: yes
                // description: name of builder
                'name': 'builderName',
                'slaves': [
                  // required: yes
                  // description: name of slave
                  'projectSlave'
                ]
              }
            }
          ]
        }
      ]
    }
   }

requires
~~~~~~~~

.. code-block:: json
   // config of assigned buildslave
   'buildbotConfig': {
    'slave': {
      'name': 'projectSlave',
      'password': 'examplePassword'
    }
   }

slave
-----

variables
~~~~~~~~~

.. code-block:: yaml
   authConfig:
    # required: yes
    # description: private ssh key for git auth
    sshKey: |
      your
      private
      key

.. code-block:: json
   'buildbotConfig': {
    'slave': {
      // required: yes
      // description: name of administrator
      'contactName': '<string>',
      // required: yes
      // description: email of administrator
      'contactEmail': '<string>',
      // required: yes
      // description: description of instance
      'description': '<string>',
      // required: no
      // description: system group of buildbot
      'group': 'buildbot',
      // required: yes
      // description: master of this slave instance
      'master': '<string>',
      // required: yes
      // description: name of buildslave instance
      'name': '<string>',
      // required: yes
      // description: password of buildslave instance
      'password': '<string>',
      // required: no
      // description: profiles of buildbot slave
      'profiles': {
        // required: no
        // description: enables ansible profile
        'ansible': {
          'cache': {
            // required: yes
            // description: database index of redis server
            'database': '<integer>',
            // required: yes
            // description: password of redis server
            'password': '<string>',
            // required: yes
            // description: port of redis server
            'port': '<integer>',
            // required: yes
            // description: fqdn of redis server
            'server': '<string>'
          }
        },
        'gentoo-build': {
          // required: yes
          // description: fqdn of http directory listing server
          'httpHost': '<string>',
          // required: yes
          // description: fqdn of rsync server
          'rsyncHost': '<string>'
        }
      }
      // required: no
      // description: system user of buildbot
      'user': 'buildbot'
    }
   }
