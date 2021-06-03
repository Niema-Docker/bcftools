# Minimal Docker image for bcftools v1.12 + alt_vars 1.0 using Alpine base
FROM alpine:latest
MAINTAINER Niema Moshiri <niemamoshiri@gmail.com>

# install bcftools
RUN apk update && \
    apk add bash bzip2-dev g++ make python3 xz-dev zlib-dev && \
    wget -O /usr/local/bin/alt_vars.py "https://raw.githubusercontent.com/Niema-Docker/bcftools/1.12_1.0/alt_vars.py" && \
    chmod a+x /usr/local/bin/alt_vars.py && \
    wget -qO- "https://github.com/samtools/htslib/releases/download/1.12/htslib-1.12.tar.bz2" | tar -xj && \
    cd htslib-1.12 && \
    ./configure && \
    make && \
    make install && \
    cd .. && \
    wget -qO- "https://github.com/samtools/bcftools/releases/download/1.12/bcftools-1.12.tar.bz2" | tar -xj && \
    cd bcftools-1.12 && \
    ./configure --without-curses && \
    make && \
    make install && \
    cd .. && \
    rm -rf bcftools-1.12 htslib-1.12
