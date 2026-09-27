# Production Dockerfile for Cars Dealership Application
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Populate frontend build if needed and run collectstatic
WORKDIR /app/server/djangoapp
RUN python manage.py migrate --noinput
RUN python manage.py populate_data
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Start production gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "djangoapp.wsgi:application"]
