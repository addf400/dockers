FROM shumingdocker.azurecr.io/nvidia/22.10:v2

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

RUN cd /tmp && \
    wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y blobfuse fuse tmux git && \
    rm packages-microsoft-prod.deb && \
    rm -rf /var/lib/apt/lists/*

RUN pip install git+https://github.com/buaahsh/fairseq.git@moe
RUN pip install git+https://github.com/shumingma/infinibatch.git
RUN pip install iopath numpy==1.23.0 tiktoken boto3 sentencepiece scikit-learn datasets loralib simplejson jsonlines json_lines tokenizers==0.14.0 transformers==4.36.2 wandb trl
RUN pip install deepspeed

COPY entrypoint.sh /entrypoint.sh
COPY setup_ssh_server.sh /setup_ssh_server.sh
RUN chmod +x /entrypoint.sh
COPY setup_ssh_server.sh /entrypoint.sh
