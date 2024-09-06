# Variables
VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PYTHON) manage.py

# Setup virtual environment and install dependencies
setup_project:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	$(MANAGE) migrate
	$(MANAGE) loaddata fixtures/data.json

# Run the Django development server
run:
	$(MANAGE) runserver

# Apply database migrations
migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

# Lint Python code and check coding standard
lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/black .
	$(VENV)/bin/mypy . --exclude 'migrations'

# Run Django tests
test:
	$(MANAGE) test

# createsuperuser with username: rk and passwork: rk
create_test_superuser:
	$(MANAGE) createsuperuser --username=rk --email=rk@mail.com --noinput
	$(MANAGE) shell -c "from django.contrib.auth import get_user_model; CustomUser = get_user_model(); u = CustomUser.objects.get(username='rk'); u.set_password('rk'); u.save()"