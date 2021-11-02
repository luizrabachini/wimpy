# Wimpy

Events tracking application to collect and analyse data across multiple origins.


## Local Development

### Install

Create a virtualenv with python3.9 using a virtual enrironment like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv wimpy -p /usr/bin/python3.9

Configure environment variables:

    $ make configure-env

Install dependencies:

    $ make install


### Run

All dependencies are managed by [docker-compose](https://docs.docker.com/compose/install/#install-compose). To start them, execute:

    $ sudo docker-compose up

To run application inside a container, execute:

    $ sudo docker-compose --file docker-compose-app.yml build  # update image
    $ sudo docker-compose --file docker-compose-app.yml up  # launch

To run application locally, execute:

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


## To Do

- Validate json schema stored in `wimpy.events.models.EventType.data_schema`
- Apply regex to validate fields `host` and `path` of `DEFAULT_EVENT_DATA_SCHEMA`
- Store static files in external bucket and remove from `Dockerfile`
- Add generic interface of brokers to create a backend integration
- Return status 202 - Accepted when API is writing events asynchronously
