FROM archlinux:latest

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV EDITOR=nvim
ENV VISUAL=nvim

RUN pacman -Syu --noconfirm \
        bash \
        ca-certificates \
        curl \
        git \
        openssh \
        sudo \
        neovim \
        less \
        ripgrep \
        fd \
        fzf \
        jq \
        unzip \
        tar \
        gzip \
        procps-ng \
        which \
    && pacman -Scc --noconfirm

# OpenCode
RUN curl -fsSL https://opencode.ai/install | bash

ENV PATH="/root/.opencode/bin:${PATH}"

WORKDIR /workspace

CMD ["opencode"]
