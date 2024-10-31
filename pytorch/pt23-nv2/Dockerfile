FROM nvcr.io/nvidia/pytorch:24.02-py3

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y fuse tmux git wget sudo && \
    rm -rf /var/lib/apt/lists/*
