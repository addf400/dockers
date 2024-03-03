FROM shumingdocker.azurecr.io/nvidia/22.10:v2

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:asdf' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#Port 22/Port 22/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse fuse tmux && \
    rm packages-microsoft-prod.deb && \
    rm -rf /var/lib/apt/lists/*

# /etc/init.d/ssh restart
# expand ref: https://stackoverflow.com/questions/41544989/docker-container-cant-use-service-sshd-restart

RUN pip install json_lines
RUN pip install transformers==4.34.0
RUN pip install tokenizers==0.14.0
RUN pip install timm==0.14.0
RUN pip install fairscale==0.14.0
RUN pip install git+https://github.com/buaahsh/fairseq.git@moe
RUN pip install git+https://github.com/shumingma/infinibatch.git
RUN pip install --user tensorboard iopath numpy==1.23.0 tiktoken boto3 sentencepiece scikit-learn datasets tensorboard deepspeed iopath einops omegaconf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
