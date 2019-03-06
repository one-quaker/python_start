#!/bin/bash

# docker+docker-compose install script for ubuntu linux
USER=`whoami`
DOCKER_COMPOSE_VERSION=1.23.2
UBUNTU_VERSION=`lsb_release -cs`


sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $UBUNTU_VERSION stable" | sudo tee /etc/apt/sources.list.d/docker.list
sudo apt update
sudo apt install docker-ce
sudo usermod -aG docker $USER
curl -L https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-`uname -s`-`uname -m` -o /tmp/docker-compose
sudo mv -v /tmp/docker-compose /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
