FROM singularitybase.azurecr.io/base/job/pytorch/acpt-rocm6.1_ubuntu20.04_py3.9_pytorch2.1.2:20240605T170411801

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y sudo && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /home/aiscuser
RUN chmod 777 /home/aiscuser
