py-compose
##########

.. image:: https://travis-ci.org/joaorafaelm/py-compose.svg?branch=master
   :target: https://travis-ci.org/joaorafaelm/py-compose

py-compose is a management tool for microservices-like or interdependent projects. With py-compose, you can declare which applications depend on each other and how they should build and run.

Usage
=====

To use py-compose, you just need to follow these 3 steps:

1. Install py-compose
2. Create ``py-compose.yaml`` configuration file
3. Use py-compose's commands, like ``py-compose up``

Installation
------------

To install, you only need to run ``pip install py-compose``.

Configuration
-------------

To configure, you need to create a ``py-compose.yaml`` with the instructions showing how py-compose should build, run and test your applications. You can also define if an app depends on others. The file content should look like this:

.. code:: yaml

    services:
        frontend_app:
            basedir: frontend
            environment:
                DEBUG: True
                BACKEND_URL: "http://localhost:8081"
            build:
                - virtualenv venv
                - ./venv/bin/pip install -r requirements.txt
            run:
                - ./venv/bin/python manage.py runserver 0.0.0.0:8080
            depends_on:
                - backend_app
            test:
                - py.test

        backend_app:
            basedir: backend
            environment:
                DEBUG:True
            build:
                - virtualenv venv
                - ./venv/bin/pip install -r requirements.txt
            run:
                - ./venv/bin/python app.py
            test:
                - py.test

Where:

basedir
    the path where py-compose will run its commands against the declared app.

environment
    environment variables to use with the declared app.

build
    list of steps to build the declared app.

run
    list of steps to run the declared app.

test
    list of steps to test the declared app.


Commands
--------

Here are a list of the py-compose useful commands.

config
^^^^^^

``py-compose config``

Show all the data extracted from the configuration file.

py-compose will search for a ``py-compose.yaml`` in the current path.
If you want to use a file in another path, use ``py-compose --file path/to/file.ext COMMAND``.

build
^^^^^

``py-compose build``

Run the build steps of all declared application.
You can run the build process for one or more specific application with ``py-compose build app1 app2 app3``.

test
^^^^

``py-compose test``

Run the test steps of all declared applications.
You can run the test process for one or more specific application with ``py-compose test app1 app2 app3``.

up
^^

``py-compose up``

Start all application running the steps declared in the configuration file.
You can start one or more specific application with ``py-compose up app1 app2 app3``.

stop
^^^^

TODO

restart
^^^^^^^

TODO

logs
^^^^

TODO

Contributing
============

TODO

License
=======

This project is licensed under the `MIT License`_.

.. _`MIT License`: https://github.com/joaorafaelm/py-compose/blob/master/LICENSE
