FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-devel

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

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd /tmp/apex && python setup.py install --cuda_ext --cpp_ext
RUN cd ~ && rm -r /tmp/apex
RUN wget https://github.com/microsoft/DeepSpeed/archive/v0.3.10.tar.gz -O /tmp/deepspeed.tar.gz && cd /tmp && tar -zxvf deepspeed.tar.gz && cd /tmp/DeepSpeed-0.3.10 && DS_BUILD_SPARSE_ATTN=1 ./install.sh -r

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse fuse && \
    rm -rf /var/lib/apt/lists/*
