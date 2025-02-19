#!/bin/bash
# scripts/update_network.sh

NEW_NETWORK=$1
OLD_NETWORK="192.168.10"

if [[ ! $NEW_NETWORK =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Invalid network format. Use: xxx.xxx.xxx"
    exit 1
fi

# Update DNS configurations
find dns/config -type f -exec sed -i "s/$OLD_NETWORK/$NEW_NETWORK/g" {} +

# Update DHCP configurations
find dhcp/config -type f -exec sed -i "s/$OLD_NETWORK/$NEW_NETWORK/g" {} +

# Update reverse zone file
OLD_REV=$(echo $OLD_NETWORK | awk -F. '{print $3"."$2"."$1}')
NEW_REV=$(echo $NEW_NETWORK | awk -F. '{print $3"."$2"."$1}')
mv dns/config/db.$OLD_REV dns/config/db.$NEW_REV

echo "Network updated to $NEW_NETWORK"
