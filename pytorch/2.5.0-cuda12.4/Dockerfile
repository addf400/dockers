FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-devel

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
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
RUN cd ~ && rm -r /tmp/apex

RUN pip install torchao
RUN MAX_JOBS=4 pip install flash-attn --no-build-isolation
