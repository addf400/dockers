FROM ubuntu:18.04

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    gcc g++ git build-essential virtualenv python3 python3-dev openssl libssl-dev libtool autoconf autogen

RUN git clone https://github.com/addf400/cmake-3.14.0.git /tmp/cmake
RUN cd /tmp/cmake && chmod 777 bootstrap && ./bootstrap --no-system-curl && make && make install
RUN apt-get install -y clang

RUN update-alternatives --install /usr/bin/cc cc /usr/bin/clang 100
RUN update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++ 100

RUN mkdir /workspace && cd /workspace && wget https://github.com/bazelbuild/bazel/releases/download/0.25.2/bazel-0.25.2-installer-linux-x86_64.sh
RUN ./bazel-0.25.2-installer-linux-x86_64.sh

RUN cd /workspace && git clone https://github.com/IntelAI/he-transformer.git
RUN cd he-transformer
RUN export HE_TRANSFORMER=$(pwd)
RUN mkdir build && cd $HE_TRANSFORMER/build && cmake .. -DCMAKE_CXX_COMPILER=clang++-6.0 && make install

RUN rm -rf /var/lib/apt/lists/*
RUN rm -rf /tmp
