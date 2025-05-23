FROM hangbo/pytorch:2.6.0cu12.4

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    libopenmpi-dev \
 && rm -rf /var/lib/apt/lists/*

RUN echo 'export PATH="/usr/local/nvidia/bin:/usr/local/cuda/bin:/opt/conda/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH"' >> /root/.bashrc
