#!/bin/bash

# Add repo for postgresql latest versions.
# Fix for NO_PUBKEY issue.
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 7FCC7D46ACCC4CF8
add-apt-repository 'deb http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

apt-get update
apt-get install -y "postgresql" "postgresql-contrib" "build-essential" "python2.7"

# This installs LTS version of Node.js v12.
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt install nodejs
npm install -g yarn

# Setup up enviroment.
ln -s /shared/code/ /home/vagrant/code
