FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install full LaTeX, Make, and MySQL dev libraries
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    pkg-config \
    default-libmysqlclient-dev \
    texlive-full \
    netcat-openbsd \
    default-mysql-client \
    && apt-get clean


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full Django project
COPY . .

# Run DB migrations, then start Django with Gunicorn
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


