---
name: m68k-toolchain-install
description: Install toolchain for m68k containing binutils, gcc and gdb 
---
# M68K Toolchain Installation Skill

## Description
Provides instructions how to download and install cross compilation developement tools for motorola m68k based processors, e.g 68000, 68331, 68020. The toolchain is installed to `/opt/toolchain68k`

## Commands

### Download and install m68k toolchain binaries
```bash
wget https://github.com/haarer/toolchain68k/releases/download/gcc152/toolchain-m68k-elf-linux-gcc-15.2.0.tar.gz 
tar xvzf <binary> -C /opt
```
Download m68k Toolchain binaries from github and install. this should work on most glibc based linuxes, but does not work on alpine (musl based)

### clone m68k toolchain source and build it
```bash
git clone https://github.com/haarer/toolchain68k.git
cd toolchain68k
bash buildtoolchain.sh linux m68k-elf

```
Download m68k Toolchain binaries from github and install. this should work on most glibc based linuxes, but does not work on alpine (musl based)


### install build dependencies
```bash
apk add bash wget git 
apk add wget
```
Install bash, wget, git, build-base needed for m68k toolchain retrieval and build

### install wget
```bash
apk add wget
```
Install wget, needed to download from the internet

### install git
```bash
apk add git
```
Install git, needed to clone repositories from the internet
## Workflow

1. **install build dependencies**
2. **download m68k toolchain** (only if glibc based linux)
3. **clone m68k toolchain source and build it** (only if on alpine linux)

