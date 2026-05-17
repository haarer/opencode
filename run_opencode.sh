#!/bin/bash
#
# This script is used to run the opencode container. 
# It will create a new container if it does not exist, otherwise it will start the existing container.
# Note that the container is run with privileged mode and access to the /dev/bus/usb device,
# which is necessary for the opencode to work properly with USB devices.
# echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", MODE="0666"' 
# sudo tee /etc/udev/rules.d/99-ftdi.rules
# sudo udevadm control --reload-rules && sudo udevadm trigger




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
    -v /dev:/dev \
    --privileged \
    --group-add keep-groups \
    --device /dev/bus/usb:/dev/bus/usb 
    --security-opt label=disable \
    --name $NAME \
    ghcr.io/anomalyco/opencode:latest
  exit 0
fi
