# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

EXPOSE 5060

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /config
COPY . /config

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /config
USER appuser
RUN mkdir -p /config && chown -R appuser:appuser /config

VOLUME ["/config"]

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5060", "main:app"]
