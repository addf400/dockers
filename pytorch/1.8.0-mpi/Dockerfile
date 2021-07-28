FROM hangbo/pytorch:1.8.0-superbench

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    vim \
    wget \
    ssh \
    tmux \
    g++ \
    llvm-9-dev \
    cmake \
 && rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse fuse && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libopenmpi-dev && rm -rf /var/lib/apt/lists/*

RUN pip install pip==9.0.0 && pip install ruamel.yaml==0.16 --disable-pip-version-check && pip install --upgrade pip
