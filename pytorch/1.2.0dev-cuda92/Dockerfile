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

RUN mkdir /app
WORKDIR /app
RUN mkdir /home/user

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
RUN conda install -y numpy ninja pyyaml mkl mkl-include setuptools cmake cffi typing
RUN conda install -y -c pytorch magma-cuda92

RUN git clone https://github.com/pytorch/pytorch ~/pytorch
RUN cd ~/pytorch && git reset --hard f176950a67adc44421a52f2fb8354e5a3cf26728 && \
    git submodule sync && \
    git submodule update --init --recursive

ENV CMAKE_PREFIX_PATH=${CONDA_PREFIX:-"$(dirname $(which conda))/../"}
RUN python setup.py install

RUN cd ~ && rm -r ~/pytorch

RUN git clone https://github.com/NVIDIA/apex ~/apex
RUN cd ~/apex && git reset --hard 1603407bf49c7fc3da74fceb6a6c7b47fece2ef8 && \
    python setup.py install --user --cuda_ext --cpp_ext
RUN cd ~ && rm -r ~/apex

RUN pip install tensorboardX six numpy tqdm path.py pandas scikit-learn py-rouge scipy

# Set the default command to python3
CMD ["python3"]
