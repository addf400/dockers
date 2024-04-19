FROM nvcr.io/nvidia/pytorch:23.11-py3

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y fuse tmux git wget && \
    rm -rf /var/lib/apt/lists/*

RUN MAX_JOBS=4 pip install -v -U git+https://github.com/facebookresearch/xformers.git@main#egg=xformers
