FROM ubuntu:18.04

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    gcc g++ git wget build-essential virtualenv python3 python3-dev openssl libssl-dev libtool autoconf autogen

RUN cd /tmp && wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0.tar.gz && tar -zxvf cmake-3.14.0.tar.gz
RUN cd /tmp/cmake-3.14.0 && RUN sed '1570s/.*/cmake_options="-DCMAKE_BOOTSTRAP=1 -DCMAKE_USE_OPENSSL=ON"/' bootstrap > bootstrap.new && RUN rm bootstrap && mv bootstrap.new bootstrap && chmod 777 bootstrap && ./bootstrap --no-system-curl && make && make install
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
