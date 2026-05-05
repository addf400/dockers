FROM nvcr.io/nvidia/pytorch:26.02-py3


RUN pip install --no-cache-dir --ignore-installed --force-reinstall addftool; \
	addf fix sing; \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

