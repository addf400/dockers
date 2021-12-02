FROM pytorch/pytorch:1.7.0-cuda11.0-cudnn8-devel

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

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse fuse && \
    rm -rf /var/lib/apt/lists/*

RUN pip install torchvision==0.8.1 numpy==1.19.2 albumentations==0.4.3 opencv-python==4.1.2.30 pudb==2019.2 imageio==2.9.0 imageio-ffmpeg==0.4.2 pytorch-lightning==1.0.8 omegaconf==2.0.0 test-tube streamlit einops==0.3.0 more-itertools transformers==4.3.1 

RUN apt-get update && apt-get install -y libopenmpi-dev && rm -rf /var/lib/apt/lists/*
