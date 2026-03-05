FROM sunyt32/pytorch:25.12.13-py3


RUN set -eux; \
	printf '%s\n' 'APT::Install-Recommends "0";' 'APT::Install-Suggests "0";' > /etc/apt/apt.conf.d/99no-install-recommends; \
	export DEBIAN_FRONTEND=noninteractive; \
	apt-get update; \
	apt-get remove --purge rapidjson-dev -y; \
	apt-get remove --purge nsight-systems-cli-2025.5.1 -y; \
	rm -rf /usr/local/cuda-13.0/NsightSystems-cli-2025.5.1/; \
	rm -rf /opt/pytorch; \
	pip install --no-cache-dir --force-reinstall setuptools Werkzeug aiohttp filelock filelock fonttools jaraco.context urllib3 urllib3 wheel protobuf; \
	python -m pip install --no-cache-dir --upgrade pip setuptools wheel; \
	apt-get -y upgrade; \
	apt-get -y autoremove --purge; \
	apt-get clean; \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
