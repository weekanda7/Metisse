# Base Stage
FROM python:3.8 AS base
ENV QT_QPA_PLATFORM=offscreen

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app

# Builder Stage
FROM base AS builder

# Install system packages and Poetry
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    curl -sSL https://install.python-poetry.org | python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Set Environment Variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.4.1

# Copy only the dependency definition files and install dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install "poetry>=${POETRY_VERSION}" && \
    poetry export --without-hashes --format=requirements.txt > requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final Stage
FROM base

# Copy precompiled wheels from the builder stage and install
COPY --from=builder /app/wheels /wheels
RUN pip install -U pip && \
    pip install --no-cache /wheels/* && \
    rm -rf /wheels

RUN apt-get update && \
    apt-get install -y --no-install-recommends xvfb && \
    apt-get install -y --no-install-recommends python3-pyqt6
# Copy only necessary files for the application to run
COPY . .
