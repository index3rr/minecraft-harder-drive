#!/bin/bash
set -e

#DISK_IMG="disk.img"
PLUGIN="file_plugin.py"
NBDKIT_PORT=10809

# Load nbd kernel module
sudo modprobe nbd

# Start nbdkit in background
echo "Starting nbdkit with plugin: $PLUGIN"
nbdkit -f -v -p "$NBDKIT_PORT" python "$PLUGIN" > nbdkit.log 2>&1 &

# Wait a second for it to boot
sleep 1

# Connect to /dev/nbd0
echo "Connecting to /dev/nbd0"
sudo nbd-client localhost "$NBDKIT_PORT" /dev/nbd0