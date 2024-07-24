FROM hangbo/pytorch-2.23dev:xformers

RUN cd /tmp && \
    apt-get update && \
    apt-get install -y sudo && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /home/aiscuser
RUN chmod 777 /home/aiscuser
RUN chown 777 /home/aiscuser
