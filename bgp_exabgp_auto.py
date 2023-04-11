import docker

client = docker.from_env()

# Define the Dockerfile content as a string
dockerfile_content = """
# Use Ubuntu 20.04 as base image
FROM ubuntu:20.04

# Install necessary dependencies
#RUN apt-get update && apt-get install -y \
#    python3-pip \
#    git \
#    curl \
#    build-essential
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libssl-dev \
    libffi-dev \
    libpcre3-dev \
    libdumbnet-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Clone ExaBGP repository
RUN git clone https://github.com/Exa-Networks/exabgp.git /tmp/exabgp

# Install ExaBGP
RUN cd /tmp/exabgp && python3 setup.py install

# Clean up
RUN rm -rf /tmp/exabgp
#RUN pip3 install ExaBGP

# Copy ExaBGP configuration file
#COPY ./bgp.conf /etc/exabgp/

# Expose port for ExaBGP
EXPOSE 179

# Start ExaBGP on container launch
#CMD ["exabgp"]
"""

# Create a new Dockerfile
with open("Dockerfile", "w") as f:
    f.write(dockerfile_content)

# Build a Docker image from the Dockerfile
image, build_logs = client.images.build(path='.', tag='exa_bgp')

# Print build logs
for log in build_logs:
    print(log)

# Save the Docker image to your local Docker registry
client.images.push('exa_bgp')