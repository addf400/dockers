FROM nvidia/cuda:9.2-cudnn7-devel-ubuntu16.04

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    sudo \
    git \
    bzip2 \
    libx11-6 \
 && rm -rf /var/lib/apt/lists/*

# Create a working directory
RUN mkdir /app
WORKDIR /app

# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user

# All users can use /home/user as their home directory
ENV HOME=/home/user
RUN chmod 777 /home/user

# Install Miniconda
RUN curl -so ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-4.7.10-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh
ENV PATH=/home/user/miniconda/bin:$PATH
ENV CONDA_AUTO_UPDATE_CONDA=false

RUN conda install -y conda-build

# CUDA 9.2-specific steps
RUN conda install -y -c pytorch torchvision cudatoolkit=9.2 -c pytorch -c defaults -c numba/label/dev \
 && conda clean -ya

RUN git clone https://github.com/NVIDIA/apex ~/apex
RUN cd ~/apex && git reset --hard 53eae1986320d016ee7b347d78839dd5e96e7e93 && \
    pip install -v --no-cache-dir \
        --global-option="--cpp_ext" \
        --global-option="--cuda_ext" ./
RUN cd ~ && rm -r ~/apex

RUN pip install tensorboardX six numpy tqdm path.py pandas scikit-learn py-rouge scipy

# Set the default command to python3
CMD ["python3"]
