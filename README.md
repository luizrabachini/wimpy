# Wimpy

Events tracking application to collect data across multiple origins.

[![CircleCI](https://circleci.com/gh/luizrabachini/wimpy/tree/main.svg?style=svg)](https://circleci.com/gh/luizrabachini/wimpy/tree/main) [![Coverage Status](https://coveralls.io/repos/github/luizrabachini/wimpy/badge.svg?branch=main)](https://coveralls.io/github/luizrabachini/wimpy?branch=main)

[![Wimpy](docs/images/wimpy.png)](https://en.wikipedia.org/wiki/J._Wellington_Wimpy)


## Development

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

    $ sudo docker-compose up  # the use of sudo is unecessary according your group settings

To initialize database, execute:

    $ make migrate

To run API locally, execute:

    $ make runserver

To run consumer locally, execute:

    $ make runconsumer


### Run Inside Docker

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


## Access

- Admin: [http://localhost/admin/](http://localhost/admin/)
- API: [http://localhost/docs/](http://localhost/docs/)

The dump file stored in `contrib/data/wimpy.sql` contain a superuser created and identified by `admin` and password `123`. This user already have the following access token that can be refreshed to interact with API:

```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzNTk4MjM0OCwiaWF0IjoxNjM1ODk1OTQ4LCJqdGkiOiIxZDFjMjc5YmUwN2M0OTg3YjQ1NTlkNjhkYzMyNWY1NSIsInVzZXJfaWQiOjF9.Y8emRZ3qtCJJApMX2gvtQ5zutZ21zrre2Sp75j4qIwY
```


## To Do

- Validate json schema stored in `wimpy.events.models.EventType.data_schema`
- Apply regex to validate fields `host` and `path` of `DEFAULT_EVENT_DATA_SCHEMA`
- Store static files in external Bucket / CDN and remove from `Dockerfile`
- Add generic interface of brokers to create a backend integration to be extended
- Return status 202 - Accepted when API is writing events asynchronously
- Fork consumer process to create workers or process messages in a threadpool
- Add idempotency_key in client side to prevent race conditions
- Create a proxy to use primary/secondary database  
