# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Define build argument for the platform
ARG TARGETPLATFORM

# Install system dependencies conditionally
RUN if [ "$TARGETPLATFORM" != "linux/amd64" ]; then \
        apt-get update && apt-get install -y \
        gcc \
        libc-dev \
    ; fi \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's source code from your host to your image filesystem.
# Ensure .dockerignore is set up to ignore files you don't want to copy
COPY . .

# Metadata as key=value labels
LABEL org.opencontainers.image.source="https://github.com/corgan2222/mail2slack" \
      org.opencontainers.image.description="mail2slack" \
      org.opencontainers.image.licenses="GPL-3"

# Set environment variables
ENV END_POINT="" \
    SLACK_SENDER="" \
    ICON_URL="" \
    SLACK_FALLBACK="" \
    CHANNEL="" \
    TOKEN="" \
    MAILSERVER="" \
    MAIL_LOGIN="" \
    MAIL_PW="" \
    FOLDER="" \
    AUTHOR_LINK="" \
    TITLE_LINK="" \
    FOOTER="" \
    FOOTER_ICON="" \
    LOG_LEVEL="" 

# Run app.py when the container launches
CMD ["python", "./mail2slack.py"]
