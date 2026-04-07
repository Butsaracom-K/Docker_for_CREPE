# Use the official Python 3.10 image as the base
FROM ubuntu:22.04

# Set the working directory inside the container
WORKDIR /CREPE_Dir

#/home/namtan/ubuntu/backup_docker

# Copy the requirements file into the container and install dependencies

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3 \
    python3-dev \
    python3-pip \
    libpq-dev \
    nano \
    vim \
    && rm -rf /var/lib/apt/lists/*
# Copy the rest of the application code into the container

COPY requirements.txt .
COPY . .
COPY ./CREPE /CREPE_Dir/CREPE/

# install python package using pip command to requirements.txt into Docker
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# 6. Install dependencies
#RUN pip install -r requirements.txt

# 7. Set the command to run your script
CMD ["bash"]
