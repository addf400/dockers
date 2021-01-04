FROM hangbo/pytorch:1.2.0-cuda10-apex-blob

# Install some basic utilities
RUN apt-get update && apt-get install -y \
    libboost-all-dev \
    libprotobuf-dev \
    protobuf-compiler

RUN wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0.tar.gz -O /tmp/cmake-3.14.0.tar.gz
RUN cd /tmp && tar -zxvf cmake-3.14.0.tar.gz && cd cmake-3.14.0 && ./bootstrap && make && make install
RUN apt-get install -y clang

RUN rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/cc cc /usr/bin/clang 100
RUN update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++ 100

RUN git clone -b v3.6.0 https://github.com/microsoft/SEAL.git /tmp/SEAL
RUN cd /tmp/SEAL && cmake -DSEAL_THROW_ON_TRANSPARENT_CIPHERTEXT=OFF . && make -j && make install

RUN git clone https://github.com/microsoft/EVA.git /tmp/EVA
RUN cd /tmp/EVA && git submodule update --init && cmake . && make -j
RUN pip install python/ && cd ~ && rm -r /tmp
