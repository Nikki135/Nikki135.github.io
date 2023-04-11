import os
import docker
client = docker.from_env()
# Define the base image
base_image = "ubuntu:latest"

# Define the packages required for Ryu Controller
packages = ["git", "python-pip"]

# Define the Ryu Controller repository URL
ryu_repo = "https://github.com/osrg/ryu.git"

# Define the working directory for the Ryu Controller
working_dir = "/home/ryu"

# Define the command to start the Ryu Controller
entry_point = "/bin/bash"

# Define the ports to expose
ports = ["6633"]

# Create the Dockerfile contents
dockerfile_contents = f"""FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    git \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libz-dev \
    python3-dev

# Clone Ryu repository
RUN git clone https://github.com/osrg/ryu.git /ryu

# Install Ryu
RUN cd /ryu && python3 -m pip install .

# Expose the necessary ports
EXPOSE 6633 6653

# Start the Ryu controller
CMD [ "ryu-manager" ]

"""

# Write the Dockerfile contents to a file
with open("Dockerfile", "w") as f:
    f.write(dockerfile_contents)

image, build_logs = client.images.build(path='.', tag='ryu_bgp')

# Print build logs
for log in build_logs:
    print(log)

# Save the Docker image to your local Docker registry
client.images.push('exa_bgp')