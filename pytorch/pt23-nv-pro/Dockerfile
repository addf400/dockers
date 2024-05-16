FROM docker.io/hangbo/pytorch-2.23dev:xformers

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:asdf' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#Port 22/Port 22/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

RUN cd /tmp && \
    wget https://github.com/addf400/files/releases/download/util/blobfuse && \
    cp /tmp/blobfuse /usr/bin/blobfuse && \
    chmod 777 /usr/bin/blobfuse && \
    rm /tmp/blobfuse

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
