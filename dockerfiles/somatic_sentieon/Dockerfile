FROM cgap/cgap-ubuntu2104-py-38:0.0.1
MAINTAINER Michele Berselli (berselli.michele@gmail.com), Phil Grayson (phil.d.grayson@gmail.com)

# general updates & installing necessary Linux components
RUN apt-get update -y && apt-get install -y \
    tabix \
    libncurses-dev \
    libbz2-dev \
    liblzma-dev \
    locales

WORKDIR /usr/local/bin

# sentieon
RUN wget https://s3.amazonaws.com/sentieon-release/software/sentieon-genomics-202112.01.tar.gz && \
    tar -xzvf sentieon-genomics-202112.01.tar.gz && \
    ln -s sentieon-genomics-202112.01 sentieon

# samtools
RUN wget https://github.com/samtools/samtools/releases/download/1.9/samtools-1.9.tar.bz2 && \
    tar -xjf samtools-1.9.tar.bz2 && \
    rm -rf samtools-1.9.tar.bz2 && \
    cd samtools-1.9 && \
    ./configure && \
    make && \
    cd .. && \
    ln -s samtools-1.9 samtools

# Sentieon somatic bash scripts
COPY somatic_sentieon_tumor_only.sh .
RUN chmod +x somatic_sentieon_tumor_only.sh
COPY somatic_sentieon_tumor_normal.sh .
RUN chmod +x somatic_sentieon_tumor_normal.sh

# env paths
ENV PATH=/usr/local/bin/sentieon/bin/:$PATH
ENV PATH=/usr/local/bin/samtools/:$PATH

CMD ["bash"]

# supporting UTF-8
RUN locale-gen "en_US.UTF-8" && update-locale LC_ALL="en_US.UTF-8"
ENV LC_ALL=en_US.UTF-8
