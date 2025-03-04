FROM nvcr.io/nvidia/pytorch:25.02-py3

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y tmux git wget unzip && \
    rm -rf /var/lib/apt/lists/*
