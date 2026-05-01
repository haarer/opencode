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
  podman run -it \
    -v "$(pwd)/workspace:/workspace" \
    -v "$(pwd)/skills:/root/.config/opencode/skills" \
    --name $NAME \
    ghcr.io/anomalyco/opencode:latest
  exit 0
fi



