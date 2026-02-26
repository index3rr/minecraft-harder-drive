#!/bin/bash
set -e

# Disconnect /dev/nbd0
echo "Disconnecting /dev/nbd0"
sudo nbd-client -d /dev/nbd0

# Kill nbdkit
sudo pkill -f nbdkit
sudo pkill -f nbd-client

# remove log
sudo rm -f nbdkit.log

# Unmount /dev/nbd0
sudo umount /dev/nbd0
