#!/bin/bash
#

NAME=opencode-dev


if podman container exists $NAME; then
  echo "consecutive run"
  podman start $NAME
  podman attach $NAME
  exit 0
else
  echo "first run"
  mkdir -p opencode-config
  mkdir -p workspace
  podman run -it \
    -v "$(pwd)/workspace:/workspace" \
    -v "$(pwd)/opencode-config:/root/.config/opencode" \
    --device /dev/bus/usb \
    --group-add keep-groups \
    --security-opt label=disable \
    --name $NAME \
    ghcr.io/anomalyco/opencode:latest
  exit 0
fi



