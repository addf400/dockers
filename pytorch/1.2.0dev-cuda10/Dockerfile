FROM pytorch/pytorch:nightly-devel-cuda10.0-cudnn7

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
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd ~/apex && git reset --hard 1603407bf49c7fc3da74fceb6a6c7b47fece2ef8 && \
    python setup.py install --user --cuda_ext --cpp_ext
RUN cd ~ && rm -r ~/apex

RUN pip install tensorboardX six numpy tqdm path.py pandas scikit-learn py-rouge scipy lmdb pyarrow py-lz4framed
