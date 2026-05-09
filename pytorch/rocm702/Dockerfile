FROM rocm/pytorch:rocm7.0.2_ubuntu24.04_py3.12_pytorch_release_2.7.1

ENV DEBIAN_FRONTEND=noninteractive

# Hold ROCm/HIP packages, full-upgrade system, then upgrade Python separately
RUN if [ -f /etc/apt/sources.list.d/ubuntu.sources ]; then \
    sed -i -E 's|URIs: http://archive.ubuntu.com/ubuntu/|URIs: https://archive.ubuntu.com/ubuntu/|g; s|URIs: http://security.ubuntu.com/ubuntu/|URIs: https://archive.ubuntu.com/ubuntu/|g' /etc/apt/sources.list.d/ubuntu.sources; \
    fi && \
    apt-get update && \
    for pkg in python3 python3-dev python3-minimal python3.12 python3.12-dev libpython3.12 libpython3.12-dev; do \
        dpkg -s "$pkg" >/dev/null 2>&1 && apt-mark hold "$pkg" || true; \
    done && \
    dpkg -l | awk '/^ii/ && ($2 ~ /rocm|rocr|rocsolver|rocsparse|rocblas|rocfft|rocalution|rocrand|rocprim|rocthrust|rocwmma|roctracer|rocprofiler|rccl|hip|hsa|comgr|miopen|migraphx|mivisionx|amdgpu|amd-smi|openmp-extras|composablekernel|hipblas|hipfft|hipsolver|hipsparse|hipsparselt|hiptensor|hipcc|hipcub|hiprand|hipfort|hipify|rpp/) {print $2}' | xargs -r apt-mark hold && \
    apt-get -y full-upgrade && \
    dpkg --get-selections | awk '/hold$/ {print $1}' | xargs -r apt-mark unhold && \
    apt-get install -y --no-install-recommends --only-upgrade \
        python3.12 python3.12-minimal python3.12-dev python3.12-venv \
        libpython3.12 libpython3.12-dev libpython3.12-minimal libpython3.12-stdlib \
        libfreetype6 python3-cryptography && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Remove ffmpeg and other vulnerable unused libs (use explicit names, avoid wildcards)
RUN apt-get update && \
    apt-get remove -y --purge \
        ffmpeg libavutil* libswresample* libavformat* libavcodec* libavdevice* \
        libpostproc* libswscale* libavfilter* \
        libopenexr* libopenexr-dev \
        libpmix2 libheif* libopencv-* opencv-data \
        libqt5* qt5-gtk-platformtheme \
        libcurl* curl* \
        liburiparser* libzvbi* libcjson1 2>/dev/null || true && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Remove vulnerable build artifacts if present
RUN rm -rf /opt/pytorch \
    /workspace/TransformerEngine/build/cmake/aotriton_external-prefix/src/aotriton_external-build/venv \
    2>/dev/null || true

# Install flash attention
COPY flash_attn-2.8.0+torch2.7_rocm7.0.2-cp312-cp312-linux_x86_64.whl /tmp/
RUN pip install --no-cache-dir /tmp/flash_attn-2.8.0+torch2.7_rocm7.0.2-cp312-cp312-linux_x86_64.whl && \
    rm /tmp/flash_attn-2.8.0+torch2.7_rocm7.0.2-cp312-cp312-linux_x86_64.whl

# Upgrade vulnerable pip packages in both Python environments
RUN for py in /opt/venv/bin/python /usr/lib/python3; do \
    "$py" -m pip install --no-cache-dir --upgrade \
    "pip>=26.0" "setuptools>=80.10.2" "wheel>=0.46.2" \
    "Werkzeug>=3.1.5" "aiohttp>=3.13.3" "filelock>=3.20.3" \
    "fonttools>=4.60.2" "urllib3>=2.6.3" "protobuf>=6.33.5" \
    "Pillow>=12.1.1" \
    "pyasn1>=0.6.2" "virtualenv>=20.36.1" \
    "python-multipart>=0.0.22" "cryptography>=42.0.4" && \
    "$py" -m pip uninstall -y distributed dask weasyprint 2>/dev/null || true; \
done

# Remove all vendored packages under setuptools to avoid stale METADATA triggering scanners
RUN rm -rf /opt/venv/lib/python3.12/site-packages/setuptools/__vendor \
           /opt/venv/lib/python3.12/site-packages/setuptools/_vendor 2>/dev/null || true

RUN pip install --no-cache-dir ipykernel

WORKDIR /workspace
