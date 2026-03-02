FROM sunyt32/pytorch:25.12.13-py3


RUN set -eux; \
	printf '%s\n' 'APT::Install-Recommends "0";' 'APT::Install-Suggests "0";' > /etc/apt/apt.conf.d/99no-install-recommends; \
	export DEBIAN_FRONTEND=noninteractive; \
	apt-get update; \
	apt-get -y upgrade; \
	apt-get -y autoremove --purge; \
	apt-get clean; \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


