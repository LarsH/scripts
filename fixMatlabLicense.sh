#!/bin/bash
# This script fixes MATLAB licensing errors, due to a changed network card.
# Author: Lars Haulin, 26 nov 2014
# Return value: 1 on failure, 0 on success.

# The desired hardware mac address
DESIRED="00:1e:33:00:8d:49"

# and the actual hardware address and interface
DATA=$(ifconfig | grep '^eth.*Ethernet  HWaddr')
ADDR=$(echo "$DATA" | awk '{print $5}')
IF=$(echo "$DATA" | awk '{print $1}')

# (and we only want a single hardware address and interface)
if [ $(echo "$DATA" | wc -l) -ne 1 ] ; then
   echo 'The number of ethernet interfaces should be exactly one!'
   echo "License fixing script ($0) can not handle this situation"
   echo 'Please rewrite me to work for this new situation'
   exit 1
fi

# is compared
if [ "$ADDR" != "$DESIRED" ]; then
   # and if they don't match, we spoof the MAC address for the interface.
   echo Spoofing MAC address for licensing to work, this might need root privs.
   sudo sh -c "ifconfig $IF down
               ifconfig $IF hw ether $DESIRED
               ifconfig $IF up"
fi

# Finally, we assert that the interface has the desired mac address.
ifconfig $IF | grep $DESIRED > /dev/null
# For clarity, the return value of the script is explicit.
exit $?
