# .devcontainer/Dockerfile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install base dependencies, build tools, Git, curl, sudo, etc.
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    gnupg \
    sudo \
    build-essential \
    ca-certificates \
    apt-transport-https \
    lsb-release \
    jq \
    unzip \
    # Python build dependencies
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# --- Install Node.js & pnpm ---
ARG NODE_VERSION="20"
RUN curl -fsSL https://deb.nodesource.com/setup_${NODE_VERSION}.x | bash - \
    && apt-get update && apt-get install -y nodejs
RUN npm install -g pnpm

# --- Install Python & Poetry ---
RUN apt-get update && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip \
    && rm -rf /var/lib/apt/lists/*
# Set python3.11 as default python3
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Add poetry to root's PATH (used during build)
ENV PATH="/root/.local/bin:$PATH"

# --- Install Other Core Tools ---
RUN python3 -m pip install --upgrade pip pipx
RUN pipx install ruff
RUN pipx install sqlfluff

# --- Setup Non-Root User ---
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME --shell /bin/bash \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to non-root user
USER $USERNAME

# Add user's local bin to PATH (for pipx tools like ruff, sqlfluff, and poetry)
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

WORKDIR /workspace