FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-devel

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
    llvm-10-dev \
    cmake \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd /tmp/apex && python setup.py install --cuda_ext --cpp_ext
RUN cd ~ && rm -r /tmp/apex

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse fuse && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get libopenmpi-dev && rm -rf /var/lib/apt/lists/*
