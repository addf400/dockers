FROM pytorch/pytorch:1.2-cuda10.0-cudnn7-devel

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
    cmake \
    build-essential \
    pkg-config \
    libgoogle-perftools-dev \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd /tmp/apex && git reset --hard de6378f5dae8fcf2879a4be8ecea8bbcb9e59d5 && python setup.py install --cuda_ext --cpp_ext
RUN cd ~ && rm -r /tmp/apex

RUN pip install tensorboardX six numpy tqdm path.py pandas scikit-learn py-rouge scipy lmdb pyarrow sacremoses transformers==2.10.0

RUN cd /tmp && wget https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb && dpkg -i packages-microsoft-prod.deb && apt-get update && apt-get install -y blobfuse fuse && rm packages-microsoft-prod.deb

RUN apt-get -y remove cmake build-essential pkg-config libgoogle-perftools-dev
