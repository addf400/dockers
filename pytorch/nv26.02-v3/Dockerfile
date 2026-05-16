FROM nvcr.io/nvidia/pytorch:26.02-py3


RUN set -eux; \
	printf '%s\n' 'APT::Install-Recommends "0";' 'APT::Install-Suggests "0";' > /etc/apt/apt.conf.d/99no-install-recommends; \
	export DEBIAN_FRONTEND=noninteractive; \
	apt-get update; \
  	apt-get update -qq && apt-get install -qq -y libarchive-dev; \
    pip install blobfile tiktoken wandb numpy tensorboard libarchive-c -q; \
    pip install nvidia-nvshmem-cu13 transformers; \
    pip uninstall nvidia-cutlass-dsl nvidia-cutlass-dsl-libs-base nvidia-cutlass-dsl-libs-cu13 -y; \
	echo "torch==2.11.0a0+eb65b36914.nv26.02" > constraints.txt && pip install --pre flash-attn-4 -c constraints.txt; \
	apt-get clean; \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
