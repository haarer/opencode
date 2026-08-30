#!/bin/bash

NAME=opencode-tui-cachy

if podman container exists "$NAME"; then
    echo "consecutive run"
    podman start "$NAME"
    podman attach "$NAME"
    exit 0
else
    echo "first run"

    mkdir -p opencode-config
    mkdir -p workspace

    podman run -it \
        -v "$(pwd)/workspace:/workspace" \
        -v "$(pwd)/opencode-config:/root/.config/opencode" \
        -v /dev:/dev \
        --privileged \
        --group-add keep-groups \
        --device /dev/bus/usb:/dev/bus/usb \
        --security-opt label=disable \
        --name "$NAME" \
        opencode-cachyos

    exit 0
fi
