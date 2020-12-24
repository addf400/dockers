FROM pytorch/pytorch:nightly-devel-cuda10.0-cudnn7

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
 && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NVIDIA/apex /tmp/apex
RUN cd /tmp/apex && git reset --hard 1603407bf49c7fc3da74fceb6a6c7b47fece2ef8 && \
    python setup.py install --cuda_ext --cpp_ext
RUN cd ~ && rm -r /tmp/apex

RUN pip install boto3==1.15.0 sentencepiece==0.1.91
RUN pip install transformers==2.10.0
RUN pip install tensorboardX six numpy tqdm path.py pandas scikit-learn py-rouge scipy lmdb pyarrow py-lz4framed regex requests botocore docutils jmespath s3transfer
