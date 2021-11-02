# Wimpy

Events tracking application to collect and analyse data across multiple origins


## Local Development

### Install (Ubuntu)

Create a virtualenv with `Python 3.9` using a virtual enrironment like [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

    $ mkvirtualenv wimpy -p /usr/bin/python3.9

Install OS dependencies:

    $ make requirements-apt

Install Python dependencies:

    $ make requirements-pip

Configure environment variables:

    $ make configure-env


### Run

All application dependencies are hosted by [Docker](https://docs.docker.com/compose/install/) and managed by [Docker Compose](https://docs.docker.com/compose/install/#install-compose). To start them, execute:

    $ sudo docker-compose up

To initialize database, execute:

    $ make migrate

To run API locally, execute:

    $ make runserver

To run consumer locally, execute:

    $ make runconsumer


## Docker Development

Start dependencies using `docker-compose.yml`:

    $ sudo docker-compose up

To run API and consumer inside a container, execute:

    $ sudo docker-compose --file docker-compose-app.yml build  # update image
    $ sudo docker-compose --file docker-compose-app.yml up  # launch


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
