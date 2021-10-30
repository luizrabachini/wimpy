# Wimpy

Events tracking framework to collect and analyse data across multiple origins.


## Local Development

### Install

Create a virtualenv with python3.9 using a virtual enrironment like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv wimpy -p /usr/bin/python3.9

Configure environment variables:

    $ make configure-env

Install dependencies:

    $ make install


### Run

To run project execute:

    $ make runserver


### Test

To check code lint, execute:

    $ make lint

A helper is available to automatic fix isort issues:

    $ make isort-fix

To run unit tests, execute:

    $ make test-unit

To run integration tests, execute:

    $ make test-integration

To run a specific test, execute:

    $ make test-matching Q=[keyword]

To run all tests, execute:

    $ make test

To check vulnerabilities of dependencies, execute:

    $ make check-vulnerabilities
