#!/bin/sh

set -e

echo "Adding pcscd service to defaults"
update-rc.d pcscd defaults add

echo "Starting the pcsc daemon"
service pcscd start