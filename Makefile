DJANGO_CMD = python3 src/manage.py
SETTINGS = wimpy.config.settings


# Helpers

clean:
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "*.DS_Store" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@find . -name ".pytest_cache" -type d | xargs rm -rf
	@find . -name "*.cache" -type d | xargs rm -rf
	@find . -name "*htmlcov" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -f coverage.xml


# Install

configure-env:
	@cp -n contrib/local.env .env
	@echo 'Please configure params from .env file.'

requirements-apt:
	@sudo apt-get install $(shell cat requirements.apt | tr "\n" " ")

requirements-pip:
	@pip install --upgrade pip
	@pip install -r requirements/dev.txt

create-superuser:
	@$(DJANGO_CMD) createsuperuser

install: requirements-apt requirements-pip migrate
	@echo "[OK] Installation completed"


# Management

migrations:
	@$(DJANGO_CMD) makemigrations $(app)

migrate:
	@$(DJANGO_CMD) migrate

shell: clean
	@$(DJANGO_CMD) shell

runserver: clean
	@$(DJANGO_CMD) runserver 0.0.0.0:8000

collectstatic:
	$(DJANGO_CMD) collectstatic --noinput

compress:
	$(DJANGO_CMD) compress


# Tests

lint: clean
	@flake8 src --exclude=venv,migrations
	@isort --check src
	@make clean

isort-fix: clean
	@isort src
	@make clean

test-unit: clean
	@pytest -m "not integration" --suppress-no-test-exit-code
	@make clean

test-integration: clean
	@pytest -m integration --suppress-no-test-exit-code
	@make clean

test: test-unit test-integration

test-matching: clean
	@pytest --pdb -k$(Q)
	@make clean

check-vulnerabilities: clean
	@safety check -r requirements/dev.txt


# Helpers

create-token:
	@curl -X POST -H "Content-Type: application/json" -d '{"username": "$(user)", "password": "$(password)"}' http://localhost:8000/auth/token/

purge-db:
	@rm -f src/wimpy/db.sqlite3
	@make migrate
