# Use an official Python runtime as a parent image
 FROM python:3.11
 
 # Set the working directory in the container
 WORKDIR /app
 
 # Install system dependencies required for LaTeX and make
 RUN apt-get update && apt-get install -y \
     make \
     texlive-latex-base \
     texlive-fonts-recommended \
     ghostscript \
     postgresql-client \
     && rm -rf /var/lib/apt/lists/*
 
 
 # Copy project files into the container
 COPY . /app
 
 # Install Python dependencies
 RUN pip install --no-cache-dir -r requirements.txt
 
 
 # Run the application
 CMD ["python", "app.py"]