FROM ubuntu:20.04

# Create a working directory
WORKDIR /root

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    openvswitch-switch \
    iproute2 \
    iputils-ping \
    net-tools \
    sudo \
    lsb-release \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Clone the Mininet repository
RUN git clone https://github.com/mininet/mininet

# Install Mininet
RUN cd mininet && \
    ./util/install.sh -a

# In your Dockerfile, replace the entrypoint section:
COPY entrypoint.sh /root/entrypoint.sh
RUN chmod +x /root/entrypoint.sh

ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["bash"]
