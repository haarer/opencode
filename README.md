# Opencode Setup 

This is an experimental opencode setup to run opencode in a podman container.
This isolates changes opencode makes from the host system. 

Opencodes skills and work space are exposed to the host using the skills and workspace directories.

It contains
- some start script to run opencode in a podman container.
- some skills, initally for m68k development.
- a container definition file for a arch linux based container 

there are three options
- run opencode as service (web interface, alpine based anomalyco container)
- run opencode tui (alpine based anomalyco container)
- run opencode tui (arch based own container)

the containers are named
- opencode-dev
- opencode-tui
- opencode-tui-cachy

# Usage

## running
creates the container at first run, consecutive runs starts it only

```
sh start_opencode_tui.sh
``` 

## shell into the running container
if you need to cleanup a mess the llm made

```
podman exec -it  opencode-tui bash
``` 


## clear the container state
all installations inside the container are lost, the workspace and opencode config are kept

use this if you need to change the container configuration
``` 
podman rm opencode-tui
``` 
