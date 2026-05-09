FROM nvcr.io/nvidia/pytorch:26.02-py3


RUN set -eux; \
	printf '%s\n' 'APT::Install-Recommends "0";' 'APT::Install-Suggests "0";' > /etc/apt/apt.conf.d/99no-install-recommends; \
	export DEBIAN_FRONTEND=noninteractive; \
	apt-get update; \
	apt-get remove --purge rapidjson-dev -y; \
	apt-get remove --purge nsight-systems-cli-2026.1.1 -y; \
	rm -rf /usr/local/cuda-13/NsightSystems-cli-2026.1.1/; \
	rm -rf /opt/pytorch; \
	python -m pip install --no-cache-dir --upgrade pip setuptools; \
	python -m pip install --no-cache-dir --ignore-installed wheel; \
	pip install --no-cache-dir --force-reinstall --ignore-installed requests black setuptools Werkzeug aiohttp filelock filelock fonttools jaraco.context urllib3 urllib3 wheel protobuf pillow nbconvert pygments; \
	pip uninstall -y aiohttp onnx; \
	apt-get -y upgrade; \
	apt-get -y autoremove --purge; \
	apt-get clean; \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
