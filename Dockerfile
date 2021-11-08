FROM continuumio/miniconda3:4.6.14
ENV TERM linux
ARG DEBIAN_FRONTEND
ENV LANG en_US.UTF-8

# setup conda environment
COPY ./environment.yml /tmp/environment.yml
WORKDIR /tmp

# setup environment and path to execute using conda env binaries
RUN conda config --set channel_priority true \
    && conda env create -n covalent -f environment.yml \
    && rm -rf /opt/conda/pkgs/*
ENV PATH /opt/conda/envs/covalent/bin:$PATH
ENV PORT_NUMBER=8080

RUN mkdir /covalent
COPY . /covalent
RUN touch /covalent/.env
WORKDIR /covalent

EXPOSE $PORT_NUMBER

CMD ["python", "dash_app.py"]