FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-devel

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y fuse tmux git wget sudo && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd /tmp/apex && pip install -v --disable-pip-version-check --no-cache-dir --no-build-isolation --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" ./
RUN cd ~ && rm -r /tmp/apex
