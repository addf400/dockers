FROM nvcr.io/nvidia/pytorch:24.02-py3

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y fuse tmux git wget sudo

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/22.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse2 && \
    rm packages-microsoft-prod.deb && \
    rm -rf /var/lib/apt/lists/*

RUN wget -P /user/bin https://github.com/addf400/files/releases/download/util/azcopy
RUN chmod +x /user/bin/azcopy
