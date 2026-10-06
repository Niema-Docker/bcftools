# Minimal Docker image for bcftools using Alpine base
FROM alpine:latest

# install bcftools
RUN apk update && \
    apk add bash bzip2-dev g++ make python3 xz-dev zlib-dev && \
    wget -qO- "https://github.com/samtools/htslib/releases/download/1.24/htslib-1.24.tar.bz2" | tar -xj && \
    cd htslib-* && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    wget -qO- "https://github.com/samtools/bcftools/releases/download/1.24/bcftools-1.24.tar.bz2" | tar -xj && \
    cd bcftools-* && \
    ./configure --without-curses && \
    make && \
    make install && \
    cd .. && \
    rm -rf bcftools-* htslib-*
