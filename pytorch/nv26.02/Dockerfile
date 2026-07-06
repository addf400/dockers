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
	python -m pip uninstall -y aiohttp onnx; \
	python -m pip install --no-cache-dir --force-reinstall --ignore-installed requests black setuptools Werkzeug aiohttp mistune jupyterlab notebook filelock fonttools jaraco.context urllib3 wheel protobuf nbconvert pygments tornado aiohttp uv pillow pytest nbconvert; \
	site_pkgs="$(python -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")"; \
	pkg_list="requests black setuptools Werkzeug aiohttp mistune jupyterlab notebook filelock fonttools jaraco.context urllib3 wheel protobuf nbconvert pygments tornado uv pillow pytest aiohappyeyeballs anyio async-lru attrs beautifulsoup4 bleach certifi charset-normalizer click debugpy decorator idna ipykernel ipython jedi json5 jsonpointer jupyter-client jupyter-events jupyter-lsp jupyter-server matplotlib-inline nbclient packaging parso pathspec platformdirs prometheus-client propcache python-json-logger rpds-py six soupsieve tinycss2 traitlets typing-extensions tzdata wcwidth yarl"; \
	for pkg in $pkg_list; do \
		ver="$(python -m pip show "$pkg" 2>/dev/null | awk '/^Version: /{print $2}')"; \
		[ -n "$ver" ] || continue; \
		pat="$(printf '%s' "$pkg" | tr '.-' '__')"; \
		find "$site_pkgs" -maxdepth 1 -type d -name "${pat}-*.dist-info" ! -name "${pat}-${ver}.dist-info" -exec rm -rf {} +; \
	done; \
	apt-get remove --purge -y python3-pip python3-setuptools python3-wheel; \
	rm -rf /usr/lib/python3/dist-packages/pip*; \
	rm -rf /usr/lib/python3/dist-packages/setuptools*; \
	rm -rf /usr/lib/python3/dist-packages/pkg_resources*; \
	rm -rf /usr/lib/python3/dist-packages/wheel*; \
	apt-get -y upgrade; \
	apt-get clean; \
	rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

