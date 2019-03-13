#!/bin/bash

# docker+docker-compose install script for ubuntu linux
USER=`whoami`
DOCKER_COMPOSE_VERSION=1.23.2
UBUNTU_VERSION=`lsb_release -cs`

# install
# sh -c "$(wget https://raw.githubusercontent.com/one-quaker/python_start/master/install_docker.sh -O -)"

sudo apt update -y
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $UBUNTU_VERSION stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update -y
sudo apt install -y docker-ce
sudo usermod -aG docker $USER
curl -L https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` -o /tmp/docker-compose
sudo mv -v /tmp/docker-compose /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose


# Docker install package for mac/windows
# mac
# https://download.docker.com/mac/stable/Docker.dmg

# windows
# https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe
