
# Pull base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/venv/bin:$PATH" \
    PYTHONPATH="/code:$PYTHONPATH"

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Copy requirements file & install requirements
COPY ./requirements.txt /code/requirements.txt
# Create virtual environment and install Python dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools && \
    /venv/bin/pip install -r requirements.txt

# Copy project files
COPY . /code/


# Entrypoint
CMD ["uvicorn","api_app:app","--host","0.0.0.0","--port","8000"]
