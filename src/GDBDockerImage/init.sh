#!/bin/sh
# Fetch the jobs
wget -O /target/$TARGET $BINARY_SOURCE
wget -O /setup/setup.sh $SETUP_SOURCE
wget -O /trigger/$TRIGGER $TRIGGER_SOURCE
# lazy permissions.
chmod 777 /target/$TARGET
chmod 777 /setup/setup.sh
# Setup the environment.
/setup/setup.sh
# run the debugging server.
/tools/gdbserver 0.0.0.0:1234 $RUN_CMD /trigger/$TRIGGER
# Announce the death of this machine.
python3 /tools/announce_death.py
