# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.238.1/containers/alpine/.devcontainer/base.Dockerfile

# [Choice] Alpine version: 3.15, 3.14, 3.13
ARG VARIANT="3.15"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-alpine-${VARIANT}

# ** [Optional] Uncomment this section to install additional packages. **
# install latest python and all dependencies to build other python versions
RUN apk update \
    && apk add --no-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
        python3 \
        python3-dev \
        gcc \
        musl-dev \
        libc-dev \
        libffi-dev \
        make \
        zlib-dev \
        openssl-dev \
        readline-dev \
        ncurses-dev \
        sqlite-dev \
        bzip2-dev \
        xz-dev
    
# running apk add py3-pip results in broken pip: importlib.metadata.PackageNotFoundError: No package metadata was found for pip 
# use ensurepip to add pip
RUN python3 -m ensurepip --upgrade
RUN python3 -m pip install --upgrade pip

# install poetry for user
USER vscode

RUN curl https://pyenv.run | bash
RUN curl -sSL https://install.python-poetry.org | python3 -