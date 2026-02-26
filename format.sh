#!/bin/bash
set -e

sudo mkfs.vfat -F12 -S512 -s1 -n "HARDERDRIVE" /dev/nbd0