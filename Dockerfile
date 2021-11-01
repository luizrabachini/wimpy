# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9.2 as dependencies

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements .

# Setup the virtualenv
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN python -m pip install --no-cache-dir -r prod.txt

# --- Release with slim ----
FROM python:3.9.2-slim AS release

# Setup system
RUN apt-get update && apt-get install -y mariadb-client

# Extra python env
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH="/venv/bin:$PATH"

# Create app directory
WORKDIR /app
COPY --from=dependencies /venv /venv
ADD ./src /app

# Collect static
RUN python manage.py collectstatic --no-input
