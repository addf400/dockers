FROM pytorch/pytorch:1.4-cuda10.1-cudnn7-devel

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
    wget \
    ssh \
    libopenmpi-dev \
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd /tmp/apex && git reset --hard 11faaca7c8ff7a7ba6d55854a9ee2689784f7ca5 && \
    python setup.py install --cuda_ext --cpp_ext
RUN cd ~ && rm -r /tmp/apex

RUN pip install boto3==1.15.0 sentencepiece==0.1.91
RUN pip install tensorboardX six numpy tqdm path.py pandas scikit-learn py-rouge scipy lmdb pyarrow py-lz4framed regex requests botocore docutils jmespath s3transfer mpi4py
