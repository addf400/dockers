FROM nvcr.io/nvidia/pytorch:24.12-py3

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

RUN pip uninstall -y torch apex flash_attn pytorch-triton torch_tensorrt torchprofile torchvision

RUN pip install torch==2.8.0 --index-url https://download.pytorch.org/whl/cu126

RUN pip install triton

RUN git clone https://github.com/NVIDIA/apex /tmp/apex && \
    cd /tmp/apex && \
    CUDA_HOME=/usr/local/cuda pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
RUN cd ~ && rm -r /tmp/apex

RUN pip install torchao
RUN MAX_JOBS=4 pip install flash-attn --no-build-isolation
